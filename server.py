#!/usr/bin/env python3
"""
Local dev server for 미완독묘.

Serves the static files in this folder (index.html and its assets) and
proxies two kinds of book-lookup requests:
  - search (title/author -> candidate list): Kakao's Daum Book Search API
  - total page count for a selected book: National Library of Korea's
    Seoji (서지정보) bibliography API, looked up by ISBN/title

Why a server at all: both APIs take their key server-side (Kakao via an
`Authorization: KakaoAK {key}` header, Seoji via a `cert_key` query param),
and a plain static page calling either directly from the browser would ship
the key in every request, visible to anyone via devtools. This proxy keeps
both keys server-side (read from .env, never sent to the browser) and hands
the frontend back only the results.

Setup:
  1. cp .env.example .env
  2. Put your real keys in .env:
       KAKAO_REST_API_KEY=... (developers.kakao.com > 내 애플리케이션 > REST API 키)
       SEOJI_CERT_KEY=...     (seoji.nl.go.kr > 인증키 신청)
  3. python3 server.py
  4. Open http://localhost:8000/
"""
import http.server
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

PORT = int(os.environ.get("PORT", 8000))  # Render (and most PaaS hosts) assign this dynamically
KAKAO_SEARCH_URL = "https://dapi.kakao.com/v3/search/book"
SEOJI_SEARCH_URL = "https://www.nl.go.kr/seoji/SearchApi.do"
PAGE_NUM_RE = re.compile(r"\d+")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# override via SYNC_DATA_DIR if you attach a Render persistent disk at a different
# mount path — without one, this directory (and everyone's saved libraries) is wiped
# on every redeploy, since the service's disk is otherwise ephemeral.
SYNC_DIR = os.environ.get("SYNC_DATA_DIR") or os.path.join(BASE_DIR, "sync_data")
CODE_RE = re.compile(r"^[A-Z0-9-]{3,32}$")
MAX_SYNC_BODY_BYTES = 2 * 1024 * 1024  # 책 몇백 권 분량의 JSON도 넉넉히 들어가는 크기


def load_env(path):
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env


_ENV = load_env(os.path.join(BASE_DIR, ".env"))
KAKAO_API_KEY = os.environ.get("KAKAO_REST_API_KEY") or _ENV.get("KAKAO_REST_API_KEY", "")
SEOJI_CERT_KEY = os.environ.get("SEOJI_CERT_KEY") or _ENV.get("SEOJI_CERT_KEY", "")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        # no special-casing needed for "/" — SimpleHTTPRequestHandler already
        # serves index.html for the bare directory root by default
        if parsed.path == "/api/search-books":
            self.handle_search(parsed)
            return
        if parsed.path == "/api/book-pages":
            self.handle_book_pages(parsed)
            return
        if parsed.path == "/api/sync/load":
            self.handle_sync_load(parsed)
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/sync/save":
            self.handle_sync_save()
            return
        self.send_json(404, {"error": "not found"})

    def handle_sync_load(self, parsed):
        params = urllib.parse.parse_qs(parsed.query)
        code = (params.get("code") or [""])[0].strip().upper()
        if not CODE_RE.match(code):
            self.send_json(400, {"error": "코드 형식이 올바르지 않습니다."})
            return
        path = os.path.join(SYNC_DIR, f"{code}.json")
        if not os.path.exists(path):
            self.send_json(404, {"error": "해당 코드로 저장된 서재를 찾을 수 없어요."})
            return
        with open(path, encoding="utf-8") as f:
            self.send_json(200, json.load(f))

    def handle_sync_save(self):
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_SYNC_BODY_BYTES:
            self.send_json(400, {"error": "요청 크기가 올바르지 않습니다."})
            return
        try:
            payload = json.loads(self.rfile.read(length))
        except Exception:
            self.send_json(400, {"error": "요청 본문이 올바른 JSON이 아닙니다."})
            return

        code = str(payload.get("code", "")).strip().upper()
        if not CODE_RE.match(code):
            self.send_json(400, {"error": "코드 형식이 올바르지 않습니다."})
            return

        os.makedirs(SYNC_DIR, exist_ok=True)
        record = {
            "name": payload.get("name", ""),
            "customName": bool(payload.get("customName")),
            "avatar": payload.get("avatar") or "",
            "books": payload.get("books") or [],
            "archive": payload.get("archive") or [],
        }
        final_path = os.path.join(SYNC_DIR, f"{code}.json")
        # 동시에 여러 기기가 저장/조회할 수 있으니, 임시 파일에 다 쓴 뒤 원자적으로 교체한다 —
        # 그래야 조회 요청이 저장 도중의 반쯤 쓰인 파일을 읽는 일이 없다.
        tmp_path = final_path + f".{os.getpid()}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False)
        os.replace(tmp_path, final_path)
        self.send_json(200, {"ok": True})

    def handle_search(self, parsed):
        if not KAKAO_API_KEY:
            self.send_json(500, {"error": "서버에 KAKAO_REST_API_KEY가 설정되어 있지 않습니다. .env를 확인해주세요."})
            return

        params = urllib.parse.parse_qs(parsed.query)
        query = (params.get("query") or [""])[0].strip()
        if not query:
            self.send_json(400, {"error": "query 파라미터가 필요합니다."})
            return
        size = (params.get("size") or ["10"])[0]

        upstream_qs = urllib.parse.urlencode({"query": query, "size": size})
        req = urllib.request.Request(
            f"{KAKAO_SEARCH_URL}?{upstream_qs}",
            headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                self.send_json(resp.status, json.loads(resp.read()))
        except urllib.error.HTTPError as e:
            try:
                detail = json.loads(e.read())
            except Exception:
                detail = {"error": str(e)}
            self.send_json(e.code, detail)
        except Exception as e:
            self.send_json(502, {"error": f"카카오 API 호출에 실패했습니다: {e}"})

    def handle_book_pages(self, parsed):
        # 카카오 검색 결과에는 전체 쪽수가 없으므로, 사용자가 검색 결과를 고른 시점에
        # 국립중앙도서관 서지정보로 쪽수만 보충 조회한다. 못 찾으면 pages: null을 돌려주고
        # 프런트엔드가 기존처럼 직접 입력 폴백을 그대로 쓰게 한다.
        if not SEOJI_CERT_KEY:
            self.send_json(200, {"pages": None})
            return

        params = urllib.parse.parse_qs(parsed.query)
        isbn = (params.get("isbn") or [""])[0].strip()
        title = (params.get("title") or [""])[0].strip()
        if not isbn and not title:
            self.send_json(400, {"error": "isbn 또는 title 파라미터가 필요합니다."})
            return

        pages = None
        if isbn:
            pages = self.lookup_pages_by_isbn(isbn)
        if pages is None and title:
            pages = self.lookup_pages_by_title(title)
        self.send_json(200, {"pages": pages})

    @staticmethod
    def seoji_docs(extra_params):
        qs = urllib.parse.urlencode({
            "cert_key": SEOJI_CERT_KEY,
            "result_style": "json",
            "page_no": "1",
            **extra_params,
        })
        with urllib.request.urlopen(f"{SEOJI_SEARCH_URL}?{qs}", timeout=6) as resp:
            return json.loads(resp.read()).get("docs") or []

    @classmethod
    def lookup_pages_by_isbn(cls, isbn):
        # 카카오 isbn 필드는 "ISBN10 ISBN13"처럼 공백으로 여러 코드가 붙어 오므로,
        # 더 특정적인 13자리 코드부터 시도한다.
        codes = sorted(isbn.split(), key=len, reverse=True)
        for code in codes:
            try:
                docs = cls.seoji_docs({"page_size": "1", "isbn": code})
            except Exception:
                continue
            if docs:
                pages = cls.parse_pages(docs[0].get("PAGE"))
                if pages:
                    return pages
        return None

    @classmethod
    def lookup_pages_by_title(cls, title):
        try:
            docs = cls.seoji_docs({"page_size": "5", "title": title})
        except Exception:
            return None
        for doc in docs:
            if (doc.get("TITLE") or "").strip() == title:
                pages = cls.parse_pages(doc.get("PAGE"))
                if pages:
                    return pages
        return None

    @staticmethod
    def parse_pages(raw):
        match = PAGE_NUM_RE.search(raw or "")
        if not match:
            return None
        n = int(match.group())
        return n if n > 0 else None

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # 동기화 코드를 다시 불러올 때 브라우저가 예전 응답을 캐시해서 돌려주면 최신
        # 상태를 못 받아오므로, 이 API 응답은 항상 캐시 없이 새로 받아오게 한다.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(BASE_DIR)
    if not KAKAO_API_KEY:
        print("⚠️  KAKAO_REST_API_KEY가 없습니다. .env.example을 .env로 복사하고 키를 채워주세요.")
    if not SEOJI_CERT_KEY:
        print("⚠️  SEOJI_CERT_KEY가 없습니다. 전체 쪽수 자동 입력이 동작하지 않습니다.")
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Serving 미완독묘 on http://localhost:{PORT}/  (Ctrl+C to stop)")
        httpd.serve_forever()
