# dh_skills

Claude Code용 개인 스킬 플러그인. 반복적인 개발 패턴과 도구 사용법을 스킬로 정리하여 Claude가 일관된 방식으로 코드를 생성하도록 한다.

## 스킬 목록

| 스킬 | 설명 | 언어 |
|------|------|------|
| [commit](skills/commit/) | Conventional Commit 형식의 Git 커밋 메시지 작성 가이드 | - |
| [csharp](skills/csharp/) | C#/.NET 코딩 참조 가이드 (3단계 레퍼런스 순서 강제) | C# |
| [load-API-key](skills/load-API-key/) | 공용서버 .env 파일에서 API 키를 로드하는 표준 패턴 | Python, C#, VBA |
| [pdf2img](skills/pdf2img/) | PDF를 JPG 이미지로 변환하는 가이드 | Python |
| [dotnet-analyze](skills/dotnet-analyze/) | .NET 어셈블리(DLL/EXE) 구조 분석, 메타데이터 추출 | C# |
| [dotnet-decompile](skills/dotnet-decompile/) | .NET 어셈블리를 C# 소스코드로 디컴파일 | C# |
| [dotnet-deobfuscate](skills/dotnet-deobfuscate/) | 난독화된 .NET 어셈블리 정리 (이름 복원, 문자열 복호화) | C# |
| [dotnet-callgraph](skills/dotnet-callgraph/) | .NET 메서드 호출 관계 분석 및 시각화 | C# |
| [pdp-agent](skills/pdp-agent/) | 제품 개발 프로세스 에이전트 — 기획→리스크→구현→런칭→회고 5단계 가이드 | - |
| [python-windows-deploy](skills/python-windows-deploy/) | Python 프로젝트를 Windows 독립 실행형 콘솔 앱(.exe)으로 빌드 및 배포 | Python |
| [revision-tracker](skills/revision-tracker/) | 파일 수정 시 docs\revisions\에 수정내역 로그 생성 및 revision_history.md 인덱싱 | - |

## 디렉토리 구조

```
dh_skills/
├── README.md
├── .claude-plugin/
│   └── marketplace.json          ← 플러그인 메타데이터
├── skills/
│   ├── commit/
│   │   └── SKILL.md
│   ├── csharp/
│   │   └── SKILL.md
│   ├── load-API-key/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── shared_apikey_loader.py
│   │       ├── usage_example.py
│   │       ├── SharedApiKeyLoader.cs
│   │       ├── SharedApiKeyLoader.bas
│   │       ├── settings.ini
│   │       └── sample.env
│   ├── pdf2img/
│   │   └── SKILL.md
│   ├── dotnet-analyze/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── dotnet-decompile/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── dotnet-deobfuscate/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── dotnet-callgraph/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── pdp-agent/
│   │   ├── SKILL.md              ← 오케스트레이터 (단계 판별 → 라우팅)
│   │   └── references/
│   │       ├── planning.md       ← Phase 1: 기획
│   │       ├── risk.md           ← Phase 2: 리스크
│   │       ├── build.md          ← Phase 3: 구현
│   │       ├── launch.md         ← Phase 4: 런칭
│   │       └── retro.md          ← Phase 5: 회고
│   ├── python-windows-deploy/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── spec_template.md  ← PyInstaller spec 파일 템플릿
│   │       └── test_patterns.md  ← 배포 전 테스트 패턴
│   └── revision-tracker/
│       ├── SKILL.md
│       └── references/
│           └── templates.md      ← 수정내역 파일 및 인덱스 템플릿
├── docs/
│   └── pdp-agent/
│       ├── README.md             ← 사용 가이드
│       └── AGENT.md              ← 설계 문서
└── refcode/
    └── pdf2jpg/                  ← PDF→JPG 변환 패키지 레퍼런스 구현
```

## 스킬 형식

각 스킬은 `skills/<skill-name>/SKILL.md` 파일을 필수로 가진다.

### SKILL.md frontmatter

```yaml
---
name: skill-name                    # 필수. 디렉토리명과 동일, kebab-case
description: "Use when ..."         # 필수. 영문. 트리거 문구 포함
argument-hint: "[optional: ...]"    # 선택. 인자 힌트
allowed-tools: Bash, Read, Write    # 선택. 허용 도구 제한
---
```

### 번들 리소스

| 폴더 | 용도 |
|------|------|
| `references/` | 레퍼런스 구현 코드, 템플릿, 단계별 에이전트 파일 |
| `scripts/` | 셋업/자동화 스크립트 |

SKILL.md 본문에서 번들 파일을 명시적으로 참조해야 한다.
