# 쌓이는 책 (Unread Cairn) Design System — Structure & Rules (Color Values Pending)

*이 문서는 오늘의집(Ohouse) 참고 DESIGN.md의 문서 구조와 작성 규칙을 그대로 따르되, 내용은 우리가 만든 `unread-cairn.html` 코드베이스를 1차 자료로 삼아 다시 쓴 문서입니다. 색상은 토큰 이름만 정의하고 값은 비워둡니다.*
*This document follows the exact section structure and authoring rules of the Ohouse reference DESIGN.md, but its content is rewritten from our own `unread-cairn.html` codebase as first-party source. Colors are defined as token names only; values are left pending.*

<!-- design-md:section experience -->
## 1. Experience

### Visual Theme & Atmosphere

**한국어.** "쌓이는 책"은 개인이 자신의 읽지 못한 책을 기록하기 위해 만든 도구입니다. 안 읽은 책을 물리 기반으로 낙하·정착시켜 돌무덤(케언) 형태로 쌓는 것이 핵심 상호작용이며, 화면은 스크롤 없이 한 화면 안에 항상 전체가 보이도록 축소되는 방식을 씁니다. 이 문서는 실제로 작성된 코드에서 값을 그대로 가져온 1차 자료 기반 기록이며, 참고 문서(오늘의집 DESIGN.md)처럼 웹사이트를 관찰해 역으로 추출한 문서가 아닙니다.

**English.** "쌓이는 책 (Unread Cairn)" is a personal tool for tracking unread books. The core interaction is physics-based: books fall and settle into a cairn. The screen always scales to fit everything without scrolling. Unlike the reference document (Ohouse's DESIGN.md), which reverse-engineers a live website, this document is a first-party record pulled directly from code we authored.

**Evidence boundary.** 코드 저장소 하나(`unread-cairn.html`)만 대상으로 하며, 별도의 공개 디자인 시스템이나 토큰 익스포트는 존재하지 않습니다. 색상 값은 아직 결정되지 않았으므로 이 문서에서 다루지 않습니다. / A single code artifact (`unread-cairn.html`) is the only source; no separate public design-system or token export exists. Color values are not yet decided and are out of scope for this document.

**Defined characteristics / 정의된 특징:**

- 캔버스와 잉크는 순백/순검정이 아닌 따뜻한 중성 톤 계열로 정의되어 있다 (`--bg`, `--ink`). / Canvas and ink are defined as warm-neutral tones, not pure white/black (`--bg`, `--ink`).
- `--accent`는 진행률 채움과 "완독" 버튼에만 쓰이는 절제된 포인트 컬러 역할이다 — 브랜드 컬러가 아니다. / `--accent` is a restrained accent used only for progress fill and the "mark as read" button — not a brand color.
- 로드되는 서체는 `Noto Serif KR`(제목류)와 `Noto Sans KR`(본문/UI)이다. / The loaded typefaces are `Noto Serif KR` (headings) and `Noto Sans KR` (body/UI).
- 돌(stone)은 6–8각 다각형이며 물리 바디 좌표와 화면 렌더링 좌표가 동일하다. / Stones are 6–8-sided polygons whose physics-body coordinates match their rendered coordinates exactly.
- 반경(radius)은 대부분 9–20px이며, FAB·아이콘 버튼만 50% 완전 원형이다. / Radii are mostly 9–20px; only the FAB and icon buttons use a full 50% circle.

### Do's and Don'ts

### Do

- 무채색·중성 톤 팔레트 방향을 유지한다. / Keep the neutral, muted palette direction.
- 물리 기반 낙하·정착 인터랙션을 핵심 정체성으로 유지한다. / Keep physics-based falling and settling as the core identity.
- `--accent`를 진행률/완독 버튼처럼 의미 있는 순간에만 아껴서 쓴다. / Reserve `--accent` for meaningful moments only (progress, "mark as read").
- 스크롤 없이 한 화면에 다 보이는 원칙(필요 시 축소)을 지킨다. / Preserve the no-scroll, scale-to-fit principle.

### Don't

- 오늘의집의 `#00a1ff` 같은 채도 높은 단일 브랜드 컬러 역할을 만들지 않는다. / Don't create a saturated single "brand color" role like Ohouse's `#00a1ff`.
- 완독 처리와 삭제를 같은 버튼·같은 무게로 섞지 않는다. / Don't collapse "mark as read" and "delete" into one button of equal weight.
- 이 문서에 실제 hex 값을 미리 채워 넣지 않는다. / Don't pre-fill real hex values in this document.
- 정적 디자인 툴(Figma 등)에 애니메이션·물리 효과까지 그대로 옮기려 하지 않는다. / Don't expect a static design tool to capture animation or physics.

### Brand Narrative

**한국어.** 이 앱은 회사나 브랜드가 아니라 한 사람의 "안 읽은 책" 기록 습관을 위한 개인 도구입니다. 그래서 기업 스토리 대신 사용 습관의 흐름을 기준으로 삼습니다: 책을 쌓고 → 가끔 무덤을 들여다보고 → 다 읽으면 무덤에서 내려놓고 → 완독 기록에 남긴다.

**English.** This is not a company or brand — it is a personal tool for one person's unread-book habit. Instead of a corporate story, the narrative anchor is the usage flow: pile a book up → occasionally look at the mound → take a stone down when finished → leave a mark in the completed-reading record.

### Principles

1. **쌓임을 정직하게 보여준다 / Show the pile honestly.** *UI implication:* 무덤은 항상 실제 등록된 권수만큼 보여야 한다. / The cairn must always visually reflect the real registered count.
2. **완독과 포기를 구분한다 / Distinguish finishing from giving up.** *UI implication:* "완독 처리"와 "삭제"는 서로 다른 버튼, 다른 결과(완독 기록 vs 소멸)를 가진다. / "Mark as read" and "delete" are separate buttons with separate outcomes (archive vs. removal).
3. **방해하지 않는다 / Don't nag.** *UI implication:* 카피는 담담하고 다정한 톤을 유지하며, 죄책감을 유발하지 않는다. / Copy stays calm and warm, never guilt-tripping.

### Personas

**한국어.** 공식적인 페르소나 리서치는 없으며, 사용 맥락은 두 가지로 나뉩니다:

- **쌓는 사람:** 책을 발견하고 등록하는 순간.
- **꺼내는 사람:** 오늘 뭘 읽을지 고르거나, 다 읽은 책을 정리하는 순간.

**English.** No formal persona research exists; usage context splits into two moments:

- **The piler:** discovering and registering a book.
- **The retriever:** picking what to read today, or archiving a finished book.

<!-- design-md:section foundations -->
## 2. Foundations

<!-- design-md:claim foundations kind=rules-or-constraints lang=ko -->
### Color Palette & Roles

아래 값은 코드(`:root` CSS 변수)에 이미 존재하는 토큰 이름과 역할입니다. 실제 오늘의집 문서처럼 "관찰값"이 아니라 "코드에 정의된 이름"이며, hex 값은 의도적으로 비워둡니다. / The values below are token names and roles already present in the code (`:root` CSS variables). Unlike the Ohouse document's "observed values," these are "names defined in code," and hex values are deliberately left blank.

### Defined tokens and surfaces

- **`--bg` (캔버스 / canvas):** 앱 전체 배경. 값 미정. / App-wide background. Value pending.
- **`--bg-soft` (보조 표면 / secondary surface):** 진행률 박스, 빈 상태 배경. 값 미정. / Progress block, empty-state background. Value pending.
- **`--panel` (패널 / panel):** 모달·시트 표면. 값 미정. / Modal and sheet surface. Value pending.
- **`--ink` (전경 / foreground):** 기본 텍스트, 기본 버튼 배경. 값 미정. / Primary text, primary button fill. Value pending.
- **`--ink-soft` (보조 텍스트 / muted text):** 메타 정보, 설명. 값 미정. / Metadata, descriptions. Value pending.
- **`--ink-faint` (희미한 텍스트 / faint text):** 플레이스홀더, 비활성 아이콘. 값 미정. / Placeholders, faint icons. Value pending.
- **`--line` (헤어라인 / hairline):** 테두리, 구분선. 값 미정. / Borders, dividers. Value pending.
- **`--stone-1`, `--stone-2`, `--stone-3` (돌 스케일 / stone scale):** 밝음→어두움 무채색 그라데이션, 돌과 표지 placeholder에 사용. 값 미정. / Light-to-dark neutral gradient, used for stones and cover placeholders. Values pending.
- **`--stone-edge` (돌 외곽선 / stone stroke):** 돌 도형의 테두리 선. 값 미정. / Outline stroke for stone shapes. Value pending.
- **`--accent` (포인트 / accent):** 진행률 채움, "완독" 버튼 전용. 값 미정. / Progress fill and "mark as read" button only. Value pending.
- **`--danger` (파괴적 동작 / destructive):** 삭제 재확인 상태 전용. 값 미정. / Delete re-confirmation state only. Value pending.

### Unresolved roles

- 성공/에러/포커스/비활성 등 상태별 색은 정의되지 않았습니다. / Success, error, focus, and disabled-state colors are not defined.
- 다크모드 토큰 세트는 없습니다. / No dark-mode token set exists.
- 색상 방향(따뜻한 종이·돌 톤, 절제된 포인트 컬러)은 채팅에서 합의된 내용이지만, 이 문서에는 아직 hex로 기록되지 않았습니다. / The color direction (warm paper/stone tones, restrained accent) was agreed in chat but is not yet recorded here as hex.
<!-- design-md:claim-end -->

### Depth & Elevation

**한국어.** 정의된 그림자 규칙: 떠 있는 요소(토스트, FAB)에 쓰이는 2단 그림자 토큰(`--shadow`); 돌은 hover 시 그림자가 커짐; 시트/모달은 아래에서 위로 뜨는 큰 그림자; 표지 썸네일은 작고 낮은 그림자; 바닥/빈 상태 등 평면 요소는 그림자 없음.

**English.** Defined shadow rules: a two-layer shadow token (`--shadow`) for floating elements (toast, FAB); stones gain a larger shadow on hover; sheets/modals use a large upward-cast shadow; cover thumbnails use a small, low shadow; flat elements (ground, empty state) have no shadow.

### Motion & Easing

**한국어.** 정의된 모션: 오버레이/시트 열고 닫기(0.2s ease); 무덤 전체 축소(0.5s, 감속 커스텀 커브); 롤링 추천 릴(3.4s, 감속 커스텀 커브); 토스트(0.25s ease); 버튼/카드 hover(0.15s ease). reduced-motion 대응은 정의되지 않았습니다.

**English.** Defined motion: overlay/sheet open-close (0.2s ease); pile scale-to-fit (0.5s, decelerating custom curve); recommendation reel roll (3.4s, decelerating custom curve); toast (0.25s ease); button/card hover (0.15s ease). Reduced-motion handling is not defined.

<!-- design-md:section typography-assets -->
## 3. Typography & Assets

### Typography Rules

### Font evidence classes

**한국어.**
- **실제 로드·사용:** `Noto Serif KR` (제목/감성적 순간), `Noto Sans KR` (본문/UI). 둘 다 Google Fonts에서 로드.
- **폴백만 존재:** 시스템 산세리프 스택 — 웹폰트 로드 실패 시에만 보임.
- **아직 없음:** 별도 아이콘 폰트, 커스텀 서브셋.

**English.**
- **Actually loaded & used:** `Noto Serif KR` (headings), `Noto Sans KR` (body/UI). Both loaded via Google Fonts.
- **Fallback only:** system sans stack — visible only if the web font fails to load.
- **Not present yet:** a dedicated icon font, custom subset builds.

### Defined hierarchy

| Role | Family | Size | Weight | Line height | Tracking | Defined scope |
|------|--------|------|--------|-------------|----------|---------------|
| Eyebrow (`UNREAD`) | Noto Sans KR | 11px | 500 | normal | 0.16em | 헤더 최상단 라벨 1개 / 1 header label |
| App title (`쌓이는 책`) | Noto Serif KR | 26px | 600 | normal | -0.01em | 헤더 h1 1개 / 1 header h1 |
| Section label | Noto Serif KR | 14.5px | 600 | normal | normal | 섹션 타이틀 1개 / 1 section title |
| Sheet header | Noto Serif KR | 17px | 600 | normal | normal | 모달 헤더 전체 / all modal headers |
| Detail title | Noto Serif KR | 18px | 600 | 1.35 | normal | 상세보기 책 제목 / detail-view book title |
| Stone label | Noto Serif KR | 9–12.5px (동적/dynamic) | 500 | 1.15 | normal | 돌 위 책 제목 전체 / all stone labels |
| Body / description | Noto Sans KR | 12–14px | 400 | 1.5–1.6 | normal | 설명, 메타 정보 전체 / all descriptions & metadata |
| Button / CTA text | Noto Sans KR | 12–14.5px | 500 | normal | normal | 버튼 라벨 전체 / all button labels |
| Input label | Noto Sans KR | 12px | 400 | normal | normal | 폼 라벨 전체 / all form labels |

<!-- design-md:section components-states -->
## 4. Components & States

### Component Stylings

이 컴포넌트들은 코드에 직접 정의된 대표 컨트롤이며, 상태 변형은 실제로 코드에 존재하는 것만 표기합니다. / These are the representative controls directly defined in code; only state variants that actually exist in code are noted.

### Buttons

**Primary (ink) button**
- Background: `--ink`
- Text: `--bg`
- Border: `0px`
- Radius: `9–10px`
- Padding: `12px`
- Font: `13–14.5px / 500 / Noto Sans KR`
- Use: "무덤에 올리기", "굴리기" 등 주요 액션 / main actions ("add to pile", "roll")

**Accent button**
- Background: `--accent`
- Text: `white` (고정값, 별도 토큰 없음 / fixed, no dedicated token)
- Border: `0px`
- Radius: `10px`
- Padding: `12px`
- Font: `14px / 500 / Noto Sans KR`
- Use: "다 읽었어요" (완독 처리), 앱 내 유일한 accent 버튼 / "mark as read" — the only accent-colored button in the app

**Outline/utility button**
- Background: `--panel`
- Text: `--ink-soft`
- Border: `1px solid var(--line)`
- Radius: `10px`
- Padding: `12px`
- Font: `13.5px / 400 / Noto Sans KR`
- Use: "이 책 무덤에서 빼기" (삭제) 기본 상태 / "delete" button, default state
- **State variant:** 첫 클릭 시 배경 `--danger` + 흰 글씨로 전환, "정말 삭제할까요?" 문구로 변경, 3초 후 자동 원복 / on first click, switches to `--danger` background with white text and a "are you sure?" label, auto-reverting after 3 seconds

**Pill button**
- Background: `--panel`
- Text: `--ink-soft`
- Border: `1px solid var(--line)`
- Radius: `20px`
- Padding: `6px 12px`
- Font: `12px / 400 / Noto Sans KR`
- Use: "🎲 오늘 뭐 읽지?", 하단 탭 / recommend trigger, bottom tabs

**Icon circular button**
- Background: `--bg-soft`
- Text: `--ink-soft`
- Border: `0px`
- Radius: `50%`, `30×30px`
- Padding: `0px`
- Font: `16px / 400`
- Use: 모달 닫기(✕) / modal close (✕)

**FAB (floating action button)**
- Background: `--ink`
- Text: `--bg`
- Border: `0px`
- Radius: `50%`, `52×52px`
- Padding: `0px`
- Shadow: `--shadow`
- Font: `24px / 300`
- Use: 책 추가(+) / add book (+)

### Inputs

**Text / number input**
- Background: `--bg`
- Text: `--ink`
- Border: `1px solid var(--line)` (focus 시 `--ink-faint`로 전환 / switches to `--ink-faint` on focus)
- Radius: `9–10px`
- Padding: `9–11px 12–14px`
- Font: `13–14px / 400 / Noto Sans KR`
- Use: 검색어, 제목/저자, 전체 쪽수, 읽은 쪽수 / search query, title/author, total pages, pages read

### Content shells

**Sheet (바텀시트 / bottom sheet)**
- Background: `--panel`
- Text: `--ink`
- Border: `0px`
- Radius: `18–20px` (상단만, 데스크톱은 전체 / top corners only; full radius on desktop)
- Padding: `20px`
- Font: 내부 콘텐츠에 따라 다름 / varies by inner content
- Use: 책 추가, 상세보기, 랜덤 추천 모달 전체 / all add/detail/recommend modals

**Progress block**
- Background: `--bg-soft`
- Text: `--ink`
- Border: `0px`
- Radius: `12px`
- Padding: `14px 16px`
- Font: 내부 콘텐츠에 따라 다름 / varies by inner content
- Use: 상세보기 내 진행률 영역 1개 / the progress area inside detail view

**Stone / list row**
- Background: `--stone-1` / `-2` / `-3` (돌), `transparent` (리스트 행 / list row)
- Text: `--ink`
- Border: `0.75px solid var(--stone-edge)` (돌만 / stones only)
- Radius: `해당 없음, 다각형/썸네일 형태 / n/a — polygon or thumbnail shape`
- Padding: `0px`
- Font: `9–14px, 컨텍스트에 따라 / context-dependent`
- Use: 무덤의 돌 전체, 검색·완독 리스트 행 전체 / all cairn stones, all search/archive list rows

### Not defined

- 에러/유효성 검사 스타일 (잘못된 입력은 토스트로만 안내, 인풋 자체 스타일 변화 없음). / Error/validation styling (invalid input is only surfaced via toast, no input-level style change).
- 로딩 스켈레톤 (검색 중엔 텍스트 안내만 있음). / Loading skeleton (search shows text status only).
- 접근성 포커스 링 스타일 (브라우저 기본값 의존). / Accessible focus-ring styling (relies on browser default).

### States

**한국어.** 코드에 실제로 존재하는 상태 전환만 기록합니다: 삭제 버튼의 2단계 확인(기본 → 경고 → 삭제, 3초 후 자동 원복); 롤링 중 "굴리기" 버튼 disabled; 책 0권일 때 빈 상태(점선 원 + 안내 문구). hover 상태는 데스크톱 커서 기준으로만 존재하며, 터치 전용 눌림 효과는 버튼마다 다르게 정의되어 있어 통일되지 않았습니다.

**English.** Only state transitions that actually exist in code are recorded: the delete button's two-step confirm (default → warning → deleted, auto-reverting after 3s); the "roll" button disabled during animation; the empty state (dashed circle + copy) when there are zero books. Hover states exist only for desktop cursors; touch-specific pressed feedback is defined inconsistently across buttons.

<!-- design-md:section layout-platforms -->
## 5. Layout & Platforms

### Layout Principles

**한국어.** 모바일 우선 단일 컬럼, 최대 너비 640px 중앙 정렬. 코드에서 반복적으로 쓰인 간격 값: `4px, 6px, 8px, 9–10px, 12px, 14px, 16px, 18px, 20px, 24px, 28px, 32px`. 별도의 그리드 시스템은 없고, flexbox 기반 세로 스택 구조입니다.

**English.** Mobile-first single column, centered with a 640px max width. Spacing values repeated throughout the code: `4px, 6px, 8px, 9–10px, 12px, 14px, 16px, 18px, 20px, 24px, 28px, 32px`. No formal grid system exists — the layout is a flexbox-based vertical stack.

### Responsive Behavior

**한국어.** 실제로 테스트/정의된 뷰포트는 모바일(좁은 화면) 기준이며, 640px 이상에서는 중앙 정렬된 카드처럼 보입니다. 태블릿/데스크톱 전용 레이아웃 규칙은 없습니다.

**English.** The only viewport actively tuned is mobile (narrow width); above 640px, the layout appears as a centered card. No dedicated tablet/desktop layout rule exists.

<!-- design-md:section content-locales -->
## 6. Content & Locales

### Voice & Tone

**한국어.** 모든 카피는 한국어 "-해요체"(부드러운 존댓말)로 통일되어 있습니다. 예: "책을 무덤 위로 떨어뜨렸어요", "완독 처리했어요 📚". 죄책감을 유발하는 표현은 의도적으로 피합니다. 이모지는 아주 가끔, 감정을 살짝 더할 때만 씁니다.

**English.** All copy uses a soft, polite Korean register ("-해요체"). Examples: "책을 무덤 위로 떨어뜨렸어요" ("dropped the book onto the mound"), "완독 처리했어요 📚" ("marked as read 📚"). Guilt-inducing phrasing is deliberately avoided. Emoji are used sparingly, only to add a light emotional touch.

이것은 코드에 실제로 존재하는 카피 스타일에 대한 기록이며, 공식 콘텐츠 가이드는 아닙니다. 영문 로케일 카피 세트는 존재하지 않습니다. / This records the copy style actually present in code, not a formal content guide. No English-locale copy set exists.

<!-- design-md:section governance -->
## 7. Governance

### Agent Prompt Guide

**한국어.** 이 문서를 참고해 요청할 때는 범위를 좁게 지정하세요. 예: "`--accent` 토큰에 쓸 채도 낮은 흙빛 톤 하나만 제안해줘, 이 문서 형식은 그대로 유지해줘." 이 문서 전체를 한 번에 다시 쓰라는 요청은 피하세요.

**English.** When requesting changes based on this document, scope them narrowly — e.g. "suggest one low-saturation clay tone for the `--accent` token, keeping this document's format intact." Avoid requests to rewrite the entire document at once.

<!-- design-md:claim authority kind=evidence-backed-reconstruction lang=ko -->
### Authority

**한국어.** 이 문서는 우리가 함께 만든 `unread-cairn.html` 코드베이스를 기준으로 한 재구성 문서이며, 오늘의집(Ohouse)이나 다른 서비스의 공식 디자인 시스템에 대한 권위를 갖지 않습니다.

**English.** This document is a reconstruction based on our own `unread-cairn.html` codebase and holds no authority over Ohouse's or any other service's official design system.
<!-- design-md:claim-end -->

<!-- design-md:claim application-priority order=prompt-fact,repository-fact,system-contract,reference-inspiration lang=ko -->
### Application priority

1. **Prompt fact:** 채팅에서 직접 요청·확정한 값이나 규칙. / Values or rules directly requested/confirmed in chat.
2. **Repository fact:** 실제 코드(`unread-cairn.html`)에 이미 존재하는 사실. / Facts already present in the actual code.
3. **System contract:** 이 문서(디자인 시스템 구조). / This document (the design-system structure).
4. **Reference inspiration:** 참고 자료로서의 오늘의집 DESIGN.md — 구조적 영감일 뿐 값의 출처가 아님. / The Ohouse DESIGN.md as reference inspiration only — never a source of values.
<!-- design-md:claim-end -->

<!-- design-md:claim unknowns policy=absent-at-smallest-unresolved-boundary lang=ko -->
### Unknowns

**한국어.** 확정되지 않은 값은 가장 작은 단위(색상 하나, 상태 하나)만 비워두고, 그럴듯한 기본값으로 채우지 않습니다.

**English.** Leave only the smallest unresolved unit blank (a single color, a single state) — never fill it with a plausible-looking default.
<!-- design-md:claim-end -->

<!-- design-md:claim changes policy=review-record-validate-before-adoption lang=ko -->
### Changes

**한국어.** 이 문서를 수정할 때는 ① 채팅에서 먼저 논의 → ② 이 문서에 기록 → ③ 실제 코드(`unread-cairn.html`)에 반영, 순서로 진행합니다.

**English.** When updating this document: ① discuss it in chat first → ② record it here → ③ apply it to the actual code (`unread-cairn.html`), in that order.
<!-- design-md:claim-end -->
