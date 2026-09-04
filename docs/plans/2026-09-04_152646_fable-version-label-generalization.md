# 계획서: dh-dev 문서의 'Fable 5' 표기를 버전 없는 'Fable'로 일반화

- Date: 2026-09-04 15:26:46
- Status: Draft

> 무엇을: `skills/` 아래 문서 2개, 총 4곳의 `Fable 5` 표기를 `Fable`로 바꾼다.
> 왜: Fable 모델이 갱신돼도 문서를 다시 고치지 않게 하려고.
> 결과: 사람이 읽는 설명 텍스트만 바뀌고 동작 변화는 없다.

## 1. Requirements Summary (요구사항 요약)

- **개발 방향: 단발성(one-off)**. 한 번 고치고 끝나는 문서 표기 정리이며, 설정 파일 분리·재사용 인터페이스·자동화 스크립트를 만들지 않는다.
- 대상 저장소: `D:\001_Work\2026\017_claude\plugins\dh_skills` (브랜치 `main`)
- **저장소 상태 주의**: 이 저장소에는 이번 작업과 무관한 미커밋 변경이 이미 있다(`.mcp.json`, `hooks/hooks.json`, `skills/commit/SKILL.md`, `skills/e3d-launcher/SKILL.md`, `skills/load-API-key/SKILL.md`, `skills/pdf2img/SKILL.md` 수정분과 다수의 추적되지 않은 파일). 그래서 경로를 한정하지 않은 `git diff`는 무관한 변경까지 함께 보여주어 정상 작업도 실패로 판정된다. 이 계획서의 모든 diff 확인 명령에는 `-- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` 경로 한정을 붙이고, 범위 밖 무변경 확인은 Step 0에서 기록한 `git status --porcelain` 기준선과 비교하는 방식으로 한다.
- 바꿀 대상: 정확히 4곳

  | 번호 | 파일 | 행 |
  |---|---|---|
  | 1 | `skills/dh-dev/SKILL.md` | 3 (frontmatter `description`) |
  | 2 | `skills/dh-dev/SKILL.md` | 26 (Agent & Model Policy 표) |
  | 3 | `skills/dh-dev/SKILL.md` | 40 (Model & Effort Tiering 표, Large 행) |
  | 4 | `skills/plan-context/references/planning-workflow.md` | 21 |

- 표기 규칙: 2026-07-25 선례(`docs/revisions/2026-07-25_182150_dh-dev-opus-label-generalization.md`, "Opus 4.8" → "Opus (`opus`)")를 그대로 따른다. 즉 **버전 숫자 없는 제품군 이름 + 백틱 alias**.
- **손대지 않을 것**
  - 백틱 alias 문자열 `` `fable` ``, `` `opus` ``, `` `sonnet` `` — 그대로 둔다.
  - `docs/plans/**`, `docs/revisions/**`, `docs/plan_history.md`, `docs/revision_history.md` — 과거 기록은 당시 사실이므로 보존.
  - `skills/dh-wiki/mcp-server/node_modules/**`
  - `skills/load-API-key/references/usage_example.py` (사용자가 명시적으로 제외)
  - `plan-context.skill` (zip 빌드 산출물, 텍스트 일치 0건)
  - 예제 코드 안의 API 모델 ID 문자열 전부
  - `skills/dh-dev/SKILL.md`의 Opus·Sonnet 표기(이미 버전 없음), `skills/dh-loop/SKILL.md`의 `VERIFIER_MODEL=opus`
- 파일 인코딩: 두 파일 모두 UTF-8 유지. `skills/dh-dev/SKILL.md` 3행에는 한국어(`단발성/간단한/심화`, `기능 개선` 등)가 들어 있으므로 저장 후 한글이 깨지지 않았는지 반드시 눈으로 확인한다.

## 2. Acceptance Criteria (인수 기준)

변경 전 기준선(측정 완료, 이 값이 비교의 출발점이다):

```bash
cd "D:/001_Work/2026/017_claude/plugins/dh_skills"
grep -rniE "fable ?5" skills/ --exclude-dir=node_modules | wc -l
# 변경 전 기대값: 4
```

| # | 기준 | 판정 방법 | 변경 전 | 변경 후 |
|---|---|---|---|---|
| A1 | `skills/` 아래에 `Fable 5`/`Fable5` 표기가 남지 않는다 | 위 grep | 4 | **0** |
| A2 | `Fable` 단어 자체는 4곳 모두 살아 있다 | `grep -rnoE "Fable" skills/ --exclude-dir=node_modules \| wc -l` | 4 | **4** |
| A3 | alias 문자열 `` `fable` ``가 2곳(26행, 40행) 그대로 있다 | `grep -rnoF '\`fable\`' skills/ --exclude-dir=node_modules \| wc -l` | 2 | **2** |
| A4 | 바뀐 파일은 정확히 2개다 | `git diff --name-only -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` | – | `skills/dh-dev/SKILL.md`, `skills/plan-context/references/planning-workflow.md` |
| A5 | 추가/삭제 행 수가 각각 4행이다(내용 교체만) | `git diff --numstat -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` | – | `skills/dh-dev/SKILL.md: 3 3`, `skills/plan-context/references/planning-workflow.md: 1 1`, 합계 `4 4` |
| A6 | 범위 밖 파일이 새로 바뀌지 않았다 | Step 0의 `git status --porcelain` 기준선 파일과 작업 후 결과를 `diff`로 비교(Step 5 명령 참조) | 기준선 파일 기록 | 새로 늘어난 항목이 대상 2개 파일뿐 |
| A7 | 두 파일의 총 행 수가 변경 전과 같다 | `wc -l` 비교 | 기준선 기록 | 동일 |
| A8 | 한글이 깨지지 않았다 | 3행 읽어서 `단발성/간단한/심화`, `기능 개선` 육안 확인 | 정상 | 정상 |
| A9 | 마크다운 표의 열 개수가 유지된다 | 26·40행의 `|` 개수 비교 | 26행: 5개, 40행: 5개 | 동일 |

## 3. Implementation Steps (구현 지침)

> 실행자는 아래 문자열을 **그대로 복사**해서 쓴다. 새로 지어내지 말 것.
> 각 변경은 정확 문자열 치환으로 한 곳씩 처리한다.
> 파일 전체를 다시 쓰지 말 것(재작성은 다른 행을 훼손할 위험이 있다).

### Step 0 — 기준선 기록

이 저장소에는 이번 작업과 무관한 미커밋 변경이 이미 있다. 그래서 "범위 밖이 안 바뀌었다"를
경로 한정 diff로는 확인할 수 없다. 대신 **작업 전 전체 dirty 목록을 기준선 파일로 남겨** 두고,
작업 후 같은 명령 결과와 비교해 **새로 늘어난 항목이 대상 2개 파일뿐인지**를 확인한다.

```bash
cd "D:/001_Work/2026/017_claude/plugins/dh_skills"

# 기준선 파일을 둘 곳(저장소 밖). Step 5와 6절에서 같은 값을 쓴다.
BASE="C:/tmp/claude/D--001-Work-2026-017-claude-plugins-dh-skills/c9caf9c0-42d1-4723-a87b-1b42914475f5/scratchpad"
mkdir -p "$BASE"

# (1) 작업 전 전체 dirty 목록을 기준선으로 기록
git status --porcelain > "$BASE/git-status-before.txt"
cat "$BASE/git-status-before.txt"

# (2) 대상 2개 파일이 지금은 깨끗한지 확인(출력이 없어야 정상)
git status --porcelain skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md

grep -rniE "fable ?5" skills/ --exclude-dir=node_modules | wc -l   # 기대: 4
wc -l skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md
```

`wc -l` 결과를 메모해 둔다(Step 5의 A7 확인에 쓴다).
`$BASE/git-status-before.txt`는 지우지 말 것(Step 5의 A6 확인에 쓴다).

### Step 1 — `skills/dh-dev/SKILL.md` 3행 (frontmatter description)

찾을 문자열 (before, 이 부분만 유일하게 일치한다):

```
Medium default: Opus at high reasoning effort, Large: Fable 5 at max reasoning effort
```

바꿀 문자열 (after):

```
Medium default: Opus at high reasoning effort, Large: Fable at max reasoning effort
```

주의: 3행은 아주 긴 한 줄이다. 위 짧은 조각만 치환하고 나머지 문장(한국어 트리거 목록 포함)은 건드리지 않는다.

### Step 2 — `skills/dh-dev/SKILL.md` 26행 (Agent & Model Policy 표)

찾을 문자열 (before):

```
Large: Fable 5 (`fable`), fallback: highest-reasoning model available (`opus`)
```

바꿀 문자열 (after):

```
Large: Fable (`fable`), fallback: highest-reasoning model available (`opus`)
```

변경 후 26행 전체(확인용, 실행자는 이 줄과 대조만 한다):

```
| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c (see Model & Effort Tiering); Medium (default): Opus (`opus`); Large: Fable (`fable`), fallback: highest-reasoning model available (`opus`); Small: Sonnet (`sonnet`) | tiered — Medium (default): `effort: "high"`; Large: maximum `effort: "max"` (ultracode-equivalent); Small: standard |
```

### Step 3 — `skills/dh-dev/SKILL.md` 40행 (Model & Effort Tiering, Large 행)

찾을 문자열 (before):

```
| Fable 5 (`fable`); fallback `opus` — `effort: "max"` |
```

바꿀 문자열 (after):

```
| Fable (`fable`); fallback `opus` — `effort: "max"` |
```

변경 후 40행 전체(확인용):

```
| **Large** | 10+ files; architectural change or a modified cross-module contract (public interface); >400 changed lines expected; or any risk-keyword hit — at least one signal must positively land here | Fable (`fable`); fallback `opus` — `effort: "max"` | Sonnet (`sonnet`) — `effort: "max"` |
```

### Step 4 — `skills/plan-context/references/planning-workflow.md` 21행

찾을 문자열 (before):

```
Large default: Fable 5, max reasoning effort
```

바꿀 문자열 (after):

```
Large default: Fable, max reasoning effort
```

변경 후 21행 전체(확인용):

```
- Run **Phase A only** (context gathering) and return the Context Summary to the orchestrator. Do **not** proceed to Phase A-2 — plan authoring is done by dh-dev's dedicated planning agent (model/effort per dh-dev's Model & Effort Tiering; Large default: Fable, max reasoning effort), not by this workflow. The Phase A-2 modes below (Interview/Direct/Consensus/Review) are never entered from dh-dev.
```

### Step 5 — 즉시 확인

Step 1~4를 마치면 아래를 실행하고 결과를 인수 기준 표와 대조한다.

```bash
cd "D:/001_Work/2026/017_claude/plugins/dh_skills"
BASE="C:/tmp/claude/D--001-Work-2026-017-claude-plugins-dh-skills/c9caf9c0-42d1-4723-a87b-1b42914475f5/scratchpad"

grep -rniE "fable ?5" skills/ --exclude-dir=node_modules | wc -l   # 기대: 0

# 경로를 한정해야 무관한 미커밋 변경이 섞이지 않는다.
git diff --name-only -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md
git diff --numstat   -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md
# 기대:
#   3       3       skills/dh-dev/SKILL.md
#   1       1       skills/plan-context/references/planning-workflow.md
#   (합계 4 4)

# 범위 밖 무변경: 작업 전 기준선과 비교해 새로 늘어난 항목만 본다.
git status --porcelain > "$BASE/git-status-after.txt"
diff "$BASE/git-status-before.txt" "$BASE/git-status-after.txt" | grep '^>'
# 기대: 아래 두 줄만 출력된다(순서는 무관).
# >  M skills/dh-dev/SKILL.md
# >  M skills/plan-context/references/planning-workflow.md
```

## 4. Code Writing Guide (코드 작성 가이드)

이번 작업은 문서 편집이므로 "코드 작성" 규칙을 문서 편집 규칙으로 읽는다.

1. **모델 표기 규칙**: 모델을 가리킬 때는 버전 숫자 없는 제품군 이름 + 필요하면 `` (`alias`) `` 형태. 보기: ``Opus (`opus`)``, ``Sonnet (`sonnet`)``, ``Fable (`fable`)``. 숫자 버전(`5`, `4.8` 등)은 문서 본문에 쓰지 않는다.
2. **alias는 문자열 그대로**: 백틱 안의 `fable`, `opus`, `sonnet`은 도구가 실제로 받는 값이다. 대소문자·철자 어느 것도 바꾸지 않는다.
3. **최소 변경**: 지정된 4개 조각 밖의 글자는 공백 하나도 바꾸지 않는다. 문장 다듬기, 오타 수정, 줄바꿈 정리 같은 "겸사겸사" 편집 금지.
4. **마크다운 표 유지**: 26행과 40행은 표의 한 행이다. `|` 구분자의 개수와 위치, 앞뒤 공백을 그대로 둔다.
5. **frontmatter 유지**: 3행은 YAML frontmatter의 `description:` 값이고 큰따옴표로 감싸여 있다. 따옴표, 콜론, 줄 구조를 건드리지 않는다.
6. **인코딩**: 두 파일 모두 UTF-8(BOM 없음)로 저장한다. 3행에는 한국어가 있으므로 저장 후 반드시 읽어서 한글이 온전한지 확인한다.
7. **줄 끝 문자**: 원본 파일의 줄 끝 방식을 유지한다. 편집 도구가 파일 전체의 줄 끝을 바꾸면 diff가 전 행으로 번지므로, 그런 일이 생기면 되돌리고 부분 치환으로 다시 한다.
8. **원문 문체 유지**: 두 파일은 영문 문서다. 한국어 문서 규칙을 적용해 영문 문장을 고치지 않는다.

## 5. Definition of Done (개발 완료조건)

| # | 완료조건 | 대응 검증 |
|---|---|---|
| D1 | `grep -rniE "fable ?5" skills/ --exclude-dir=node_modules`의 결과 행 수가 0이다 | V1 |
| D2 | `git diff --name-only -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md`가 정확히 2개 파일만 보여준다 | V2 |
| D3 | `git diff --numstat -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` 결과가 `skills/dh-dev/SKILL.md: 3 3`, `skills/plan-context/references/planning-workflow.md: 1 1`(합계 추가 4행, 삭제 4행)이다 | V2 |
| D4 | 변경 후 26행과 40행의 `|` 개수가 변경 전과 같다 | V3 |
| D5 | `` `fable` `` 백틱 alias가 `skills/dh-dev/SKILL.md`에 2회 남아 있다 | V4 |
| D6 | `skills/dh-dev/SKILL.md` 3행에 `단발성/간단한/심화`와 `기능 개선`이 깨짐 없이 보인다 | V5 |
| D7 | 두 파일에 U+FFFD나 `占쏙옙` 같은 깨짐 흔적이 없다 | V5 |
| D8 | Step 0 기준선 대비 새로 dirty가 된 파일이 대상 2개뿐이다(`docs/`, `node_modules/`, `plan-context.skill` 등이 새로 바뀌지 않았다) | V6 |
| D9 | 두 파일의 총 행 수가 Step 0 기준선과 같다 | V7 |
| D10 | 변경 후 4개 행이 3절의 "변경 후 전체" 문자열과 완전히 일치한다 | V8 |

## 6. Adversarial Test Environment (적대적 테스트 환경)

모든 명령은 Git Bash 기준이며, 저장소 최상위에서 실행한다.

```bash
cd "D:/001_Work/2026/017_claude/plugins/dh_skills"
```

### T1 — 부족 치환(누락)

```bash
grep -rniE "fable ?5" skills/ --exclude-dir=node_modules
```
통과: **아무것도 출력되지 않음**.

### T2 — 과잉 치환(범위 밖 파일까지 바뀜)

```bash
BASE="C:/tmp/claude/D--001-Work-2026-017-claude-plugins-dh-skills/c9caf9c0-42d1-4723-a87b-1b42914475f5/scratchpad"

git diff --name-only -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md

git status --porcelain > "$BASE/git-status-after.txt"
diff "$BASE/git-status-before.txt" "$BASE/git-status-after.txt" | grep '^>'
```
통과: 첫 명령이 정확히 두 줄(`skills/dh-dev/SKILL.md`, `skills/plan-context/references/planning-workflow.md`).
둘째 확인은 기준선 대비 새로 늘어난 항목이 그 두 파일뿐이어야 한다(`docs/`, `node_modules/`, `plan-context.skill`, `usage_example.py`가 새로 나타나면 실패).
경로를 한정하지 않은 `git diff --name-only`는 이 저장소에 이미 있는 무관한 미커밋 변경까지 보여주므로 판정에 쓰지 않는다.

### T3 — 과잉 치환(같은 파일 안에서 엉뚱한 곳까지 바뀜)

```bash
git diff --numstat -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md
```
통과: `skills/dh-dev/SKILL.md`가 `3 3`(3·26·40행), `skills/plan-context/references/planning-workflow.md`가 `1 1`(21행). 합계 `4 4`.

### T4 — alias 문자열 `fable` 오손상

```bash
grep -rnoF '`fable`' skills/ --exclude-dir=node_modules | wc -l   # 기대: 2
grep -rniE '`fable ?5`|`Fable`|`FABLE`' skills/ --exclude-dir=node_modules   # 기대: 출력 없음
```

### T5 — 표기가 아예 사라짐(과잉 삭제)

```bash
grep -rnoE 'Fable' skills/ --exclude-dir=node_modules | wc -l   # 기대: 4
```

### T6 — 마크다운 표 구조 깨짐

```bash
awk 'NR==26 || NR==40 {n=gsub(/\|/,"|"); print NR": pipes="n}' skills/dh-dev/SKILL.md
sed -n '22,45p' skills/dh-dev/SKILL.md
```
통과: `26: pipes=5`, `40: pipes=5`(변경 전과 동일), 표가 정상으로 보임.

### T7 — frontmatter 깨짐

```bash
sed -n '1,5p' skills/dh-dev/SKILL.md
```
통과: 1행 `---`, 3행 `description: "..."`(한 줄, 큰따옴표 짝 맞음).

### T8 — 인코딩 깨짐 / 한글 손상

```bash
PYTHONIOENCODING=utf-8 python - <<'PYEOF'
targets = [
    r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md",
    r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\planning-workflow.md",
]
bad = ["\ufffd", "占쏙옙", "ï»¿"]
for p in targets:
    with open(p, encoding="utf-8") as f:
        text = f.read()
    hits = [b for b in bad if b in text]
    print(p, "-> 깨짐표시:", hits if hits else "없음")
with open(targets[0], encoding="utf-8") as f:
    line3 = f.readlines()[2]
print("3행 한글 표본:", "단발성/간단한/심화" in line3, "|", "기능 개선" in line3)
print(line3[:220])
PYEOF
```
통과: 두 파일 모두 `깨짐표시: 없음`, `3행 한글 표본: True | True`.

### T9 — 문자열 정확성

```bash
grep -c 'Large: Fable at max reasoning effort' skills/dh-dev/SKILL.md            # 기대: 1
grep -c 'Large: Fable (`fable`), fallback' skills/dh-dev/SKILL.md               # 기대: 1
grep -c 'Fable (`fable`); fallback `opus`' skills/dh-dev/SKILL.md               # 기대: 1
grep -c 'Large default: Fable, max reasoning effort' skills/plan-context/references/planning-workflow.md   # 기대: 1
```

### T10 — 되돌리기 확인(안전망)

```bash
git checkout -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md
grep -rniE "fable ?5" skills/ --exclude-dir=node_modules | wc -l   # 되돌린 뒤 기대: 4
```

## 7. Risks and Mitigations (위험과 대응)

| # | 위험 | 가능성 | 영향 | 대응 |
|---|---|---|---|---|
| R1 | 백틱 alias `` `fable` ``까지 함께 치환해 도구 호출 값이 깨짐 | 낮음 | 큼 | 3절 before 문자열을 그대로 사용, T4로 확인. 정규식 일괄 치환 금지 |
| R2 | 3행 frontmatter를 통째로 다시 쓰다가 한국어 트리거 목록이 깨짐 | 중간 | 큼 | 짧은 조각만 치환. T7·T8로 확인 |
| R3 | 편집 도구가 줄 끝을 바꿔 diff가 전 행으로 번짐 | 중간 | 중간 | T3이 `3 3` / `1 1`이 아니면 되돌리고 재편집 |
| R4 | UTF-8이 아닌 인코딩으로 저장돼 한글이 깨짐 | 낮음 | 큼 | T8 필수 실행 |
| R5 | 범위 밖 파일까지 치환해 과거 기록을 훼손 | 중간 | 중간 | grep 범위를 `skills/`로 한정, T2의 기준선 비교로 확인 |
| R6 | 표 셀 구분자를 잘못 건드려 표가 깨짐 | 낮음 | 중간 | T6 |
| R7 | "이왕 보는 김에" 다른 문장까지 다듬어 범위가 커짐 | 중간 | 중간 | 4절 규칙 3번, T3의 합계 `4 4`로 차단 |
| R8 | `node_modules` 안 우연한 일치로 grep 결과가 흔들림 | 낮음 | 작음 | 모든 grep에 `--exclude-dir=node_modules` 고정 |
| R9 | 이 계획서 자체에 `Fable 5`가 적혀 grep 기준값이 어긋남 | 중간 | 작음 | 검증 grep 범위를 `skills/`로 한정 |
| R10 | 저장소에 이미 있는 무관한 미커밋 변경 때문에 경로 한정 없는 `git diff`가 정상 작업도 실패로 판정 | 높음 | 중간 | 모든 diff 명령에 대상 2개 파일 경로 한정을 붙이고, 범위 밖 무변경은 Step 0 기준선(`git status --porcelain`) 비교로 판정 |

## 8. Verification Steps (검증 절차)

실행 위치: `D:/001_Work/2026/017_claude/plugins/dh_skills` (Git Bash)

- **V1 — 잔여 표기 0건 (D1)**: `grep -rniE "fable ?5" skills/ --exclude-dir=node_modules | wc -l` → `0`
- **V2 — 변경 범위 (D2, D3)**: `git diff --name-only -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md`, `git diff --numstat -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` → 2개 파일, `skills/dh-dev/SKILL.md: 3 3`, `skills/plan-context/references/planning-workflow.md: 1 1`(합계 `4 4`)
- **V3 — 표 구조 (D4)**: T6 명령 → `26: pipes=5`, `40: pipes=5`
- **V4 — alias 보존 (D5)**: ``grep -rnoF '`fable`' skills/dh-dev/SKILL.md | wc -l`` → `2`
- **V5 — 인코딩·한글 무결성 (D6, D7)**: T8 파이썬 블록 → 깨짐 없음, 한글 표본 True
- **V6 — 범위 밖 무변경 (D8)**: T2 둘째 확인(`diff "$BASE/git-status-before.txt" "$BASE/git-status-after.txt" | grep '^>'`) → 기준선 대비 새로 늘어난 항목이 대상 2개 파일뿐
- **V7 — 행 수 보존 (D9)**: `wc -l` → Step 0 기준선과 동일
- **V8 — 최종 문자열 대조 (D10)**: T9 네 명령 → 모두 `1`
- **V9 — 육안 최종 확인**: `git diff -U0 -- skills/dh-dev/SKILL.md skills/plan-context/references/planning-workflow.md` → `-` 4행, `+` 4행뿐이고 각 쌍의 차이가 `Fable 5` → `Fable` 하나뿐

**결과 확인 요약**: V1이 `0`, V2가 `skills/dh-dev/SKILL.md: 3 3` / `skills/plan-context/references/planning-workflow.md: 1 1`(합계 `4 4`), V6에서 새로 늘어난 dirty 항목이 대상 2개 파일뿐, V9의 diff가 4쌍뿐이면 완료다.
