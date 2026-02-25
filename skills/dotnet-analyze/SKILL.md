---
name: dotnet-analyze
description: ".NET 어셈블리(DLL/EXE) 분석의 진입점. 구조 분석, 메타데이터 추출, 난독화 감지, 참조 어셈블리 확인을 수행한다. 사용자가 DLL 분석, EXE 리버싱, .NET 바이너리 구조 파악, 어셈블리 정보 확인, 타입/클래스/메서드 목록 조회를 요청할 때 사용한다. 'DLL 분석해줘', '이 EXE 뭐하는 건지 파악해줘', '.NET 어셈블리 구조 보여줘', '클래스 목록 뽑아줘' 같은 요청에 반드시 이 스킬을 사용하라."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET 어셈블리 구조 분석

.NET DLL/EXE 파일의 메타데이터, 타입 구조, 참조, 난독화 여부를 분석하는 스킬이다.

## 사전 요건

- .NET 8 SDK 설치 필요 (`dotnet --version`으로 확인)
- 분석 대상: .NET 관리 코드 어셈블리 (DLL 또는 EXE)

## 분석 워크플로우

### 1단계: 환경 확인 및 프로젝트 준비

```bash
# .NET SDK 확인
dotnet --version

# 임시 분석 프로젝트가 없으면 생성
if [ ! -f "/tmp/dotnet-analyzer/DotNetAnalyzer.csproj" ]; then
  mkdir -p /tmp/dotnet-analyzer
  # scripts/setup-project.sh 실행하여 프로젝트 초기화
fi
```

프로젝트가 없으면 `scripts/setup-project.sh`를 실행하여 NuGet 패키지(ICSharpCode.Decompiler, dnlib, Spectre.Console)가 포함된 C# 콘솔 프로젝트를 생성한다.

### 2단계: 어셈블리 기본 정보 추출

다음 C# 스크립트를 생성하여 실행한다. `references/analyze-template.cs`에 전체 템플릿이 있다.

핵심 분석 항목:
- **어셈블리 이름** 및 버전
- **대상 프레임워크** (.NET Framework / .NET Core / .NET 5+)
- **런타임 버전**
- **타입 수** (클래스, 인터페이스, 열거형, 구조체, 델리게이트)
- **메서드/프로퍼티/필드 수**
- **참조 어셈블리** 목록
- **임베디드 리소스** 목록
- **난독화 감지** (알려진 도구 시그니처 + 휴리스틱)

### 3단계: 타입 구조 트리 출력

네임스페이스 → 타입 → 멤버 계층 구조를 트리 형태로 정리한다.

```
📦 MyApp.Services
  📦 UserService (Class)
    🔧 public Task<User> GetUserAsync(int id)
    🔧 public void UpdateUser(User user)
    🔹 private readonly IDbContext _db
  🔷 IUserRepository (Interface)
    🔧 Task<User> FindById(int id)
```

### 4단계: 결과 분석 및 후속 작업 제안

분석 결과에 따라 적절한 후속 스킬을 안내한다:

| 상황 | 후속 스킬 |
|------|-----------|
| 소스코드를 복원하고 싶다 | `dotnet-decompile` 스킬 사용 |
| 난독화가 감지되었다 | `dotnet-deobfuscate` 스킬 사용 |
| 호출 관계를 파악하고 싶다 | `dotnet-callgraph` 스킬 사용 |

## 난독화 감지 기준

다음 패턴으로 난독화 여부를 판별한다:

**어트리뷰트 기반** (확정적):
- `Dotfuscator`, `ConfusedBy`, `SmartAssembly`, `Eazfuscator`, `Babel`, `CryptoObfuscator`, `NETGuard`, `ILProtector`, `DeepSea`, `Agile`, `Xenocode`

**이름 패턴 기반** (휴리스틱):
- 유니코드 제어 문자 포함 → ConfuserEx 추정
- 단일 문자 이름 (a, b, c...) 다수
- 비ASCII 문자 패턴
- 모음 비율 10% 미만인 긴 이름 (Base64 유사)
- 전체 이름 중 30% 이상이 위 패턴에 해당하면 "난독화됨"으로 판정

## 출력 형식

분석 결과를 구조화된 표로 출력한다:

```
┌──────────────────────────────────────┐
│      어셈블리 분석 요약              │
├─────────────────┬────────────────────┤
│ 어셈블리        │ MyApp v1.2.3       │
│ 프레임워크      │ .NET 8.0           │
│ 타입 수         │ 47                 │
│ 메서드 수       │ 312                │
│ 참조 어셈블리   │ 12                 │
│ 난독화 감지     │ 아니오             │
└─────────────────┴────────────────────┘
```

추가로 JSON 형식 내보내기도 지원한다 (사용자 요청 시).

## 주의사항

- Native C++ DLL이나 혼합 모드 어셈블리는 완전 분석이 불가능하다
- .NET Framework 1.x 어셈블리는 일부 메타데이터 읽기가 실패할 수 있다
- 대규모 어셈블리(타입 1000+)는 분석에 수십 초가 걸릴 수 있다
