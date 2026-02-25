---
name: dotnet-decompile
description: ".NET 어셈블리(DLL/EXE)를 C# 소스코드로 디컴파일한다. IL 코드를 원본에 가까운 C# 코드로 복원하여 파일로 저장한다. '소스코드 복원', '디컴파일', 'C# 코드로 변환', 'DLL에서 코드 추출', '소스 뽑아줘', '코드 보여줘' 같은 요청에 반드시 이 스킬을 사용하라. 특정 클래스만 추출하거나 전체 어셈블리를 네임스페이스별 .cs 파일로 분리 저장하는 것도 지원한다."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET 어셈블리 디컴파일 (IL → C#)

ICSharpCode.Decompiler(ILSpy 엔진)를 사용하여 .NET 어셈블리를 C# 소스코드로 복원한다.

## 사전 요건

- .NET 8 SDK
- 공통 프로젝트 설정: `dotnet-analyze` 스킬의 `scripts/setup-project.sh`를 먼저 실행

## 디컴파일 모드

### 모드 1: 전체 어셈블리 → 단일 파일

대상 어셈블리 전체를 하나의 .cs 파일로 출력한다. 빠른 확인에 적합하다.

```csharp
using ICSharpCode.Decompiler;
using ICSharpCode.Decompiler.CSharp;

var settings = new DecompilerSettings(LanguageVersion.CSharp11)
{
    ThrowOnAssemblyResolveErrors = false,
    RemoveDeadCode = true,
    RemoveDeadStores = true,
};

var decompiler = new CSharpDecompiler(targetPath, settings);
string fullSource = decompiler.DecompileWholeModuleAsString();
File.WriteAllText(outputPath, fullSource);
```

### 모드 2: 타입별 개별 .cs 파일

네임스페이스를 디렉토리 구조로 매핑하여 각 타입을 개별 .cs 파일로 저장한다. 코드 분석에 가장 유용하다.

```csharp
var types = decompiler.TypeSystem.GetAllTypeDefinitions()
    .Where(t => !t.Name.StartsWith("<"));

foreach (var type in types)
{
    string source = decompiler.DecompileTypeAsString(new FullTypeName(type.FullName));

    // 네임스페이스 → 디렉토리
    string[] parts = type.FullName.Split('.');
    string dir = Path.Combine(outputDir, Path.Combine(parts.Take(parts.Length - 1).ToArray()));
    Directory.CreateDirectory(dir);

    string filePath = Path.Combine(dir, SanitizeFileName(parts.Last()) + ".cs");
    File.WriteAllText(filePath, source);
}
```

### 모드 3: 특정 타입만 디컴파일

사용자가 특정 클래스/인터페이스를 지정한 경우.

```csharp
string source = decompiler.DecompileTypeAsString(new FullTypeName("MyApp.Services.UserService"));
Console.WriteLine(source);
```

## 전체 스크립트 템플릿

상세 템플릿은 `references/decompile-template.cs`를 참조한다.

## 출력 구조 예시

```
decompiled_src/
├── MyApp/
│   ├── Program.cs
│   ├── Models/
│   │   ├── User.cs
│   │   └── Order.cs
│   └── Services/
│       ├── UserService.cs
│       └── OrderService.cs
└── MyApp.Data/
    ├── DbContext.cs
    └── Repositories/
        └── UserRepository.cs
```

## DecompilerSettings 주요 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `LanguageVersion` | CSharp11 | 출력 C# 버전 (최신 문법 활용) |
| `ThrowOnAssemblyResolveErrors` | false | 참조 해결 실패 시 예외 억제 |
| `RemoveDeadCode` | true | 사용되지 않는 코드 제거 |
| `RemoveDeadStores` | true | 불필요한 변수 할당 제거 |
| `ShowXmlDocumentation` | true | XML 문서 주석 포함 |
| `DecompileMemberBodies` | true | 메서드 본문 디컴파일 |

## 디컴파일 실패 처리

일부 타입은 디컴파일에 실패할 수 있다. 실패한 타입은 건너뛰고 주석으로 기록한다:

```csharp
try
{
    string source = decompiler.DecompileTypeAsString(new FullTypeName(type.FullName));
    // 저장
}
catch (Exception ex)
{
    string fallback = $"// 디컴파일 실패: {type.FullName}\n// 오류: {ex.Message}\n";
    // fallback 저장
}
```

## 난독화된 어셈블리 처리

난독화가 감지된 어셈블리는 디컴파일 전에 `dotnet-deobfuscate` 스킬로 먼저 정리하는 것을 권장한다. 난독화된 상태로 디컴파일하면 읽기 어려운 변수명과 제어 흐름이 그대로 출력된다.

## 주의사항

- 디컴파일된 코드는 원본과 100% 동일하지 않다 (컴파일러 최적화, 디버그 정보 손실)
- `async/await`, LINQ 등은 상태머신으로 변환되어 있을 수 있다
- 대규모 어셈블리(500+ 타입)는 전체 디컴파일에 수분이 걸릴 수 있다
