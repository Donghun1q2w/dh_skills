# dh_skills

Claude Code용 개인 스킬 플러그인. 반복적인 개발 패턴과 도구 사용법을 스킬로 정리하여 Claude가 일관된 방식으로 코드를 생성하도록 한다.

## 스킬 목록

| 스킬 | 설명 | 언어 |
|------|------|------|
| [commit-guide](skills/commit-guide/) | Conventional Commit 형식의 Git 커밋 메시지 작성 가이드 | - |
| [load-API-key](skills/load-API-key/) | 공용서버 .env 파일에서 API 키를 로드하는 표준 패턴 | Python, C#, VBA |
| [pdf2img](skills/pdf2img/) | PDF를 JPG 이미지로 변환하는 가이드 | Python |
| [dotnet-analyze](skills/dotnet-analyze/) | .NET 어셈블리(DLL/EXE) 구조 분석, 메타데이터 추출 | C# |
| [dotnet-decompile](skills/dotnet-decompile/) | .NET 어셈블리를 C# 소스코드로 디컴파일 | C# |
| [dotnet-deobfuscate](skills/dotnet-deobfuscate/) | 난독화된 .NET 어셈블리 정리 (이름 복원, 문자열 복호화) | C# |
| [dotnet-callgraph](skills/dotnet-callgraph/) | .NET 메서드 호출 관계 분석 및 시각화 | C# |

## 디렉토리 구조

```
dh_skills/
├── README.md
├── .claude-plugin/
│   └── marketplace.json          ← 플러그인 메타데이터
├── skills/
│   ├── commit-guide/
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
│   └── dotnet-callgraph/
│       ├── SKILL.md
│       └── references/
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
| `references/` | 레퍼런스 구현 코드, 템플릿, 설정 파일 샘플 |
| `scripts/` | 셋업/자동화 스크립트 |

SKILL.md 본문에서 번들 파일을 명시적으로 참조해야 한다.
