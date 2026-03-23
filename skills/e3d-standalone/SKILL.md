---
name: e3d-standalone
description: "AVEVA E3D Standalone mode C# development guide. Connect to E3D database, login to projects, execute PML macros, and traverse DB elements via Standalone API. Use when writing C# code for E3D automation, PDMS standalone access, PML macro execution, AVEVA database queries, or E3D batch processing. Triggers on: 'E3D', 'AVEVA standalone', 'PML macro', 'PDMS login', 'E3D automation', 'Standalone.Open', 'Standalone.Start'."
---

# E3D Standalone Development Guide

C#으로 AVEVA E3D에 Standalone 모드로 접속하여 PML 매크로를 실행하는 가이드.

## DLL References

9개 AVEVA DLL 필수. 기본 경로: `C:\cae_prog\AVEVA\v2.x\e3d\`

| DLL | 주요 네임스페이스 | 용도 |
|-----|-------------------|------|
| Aveva.Core.dll | `Aveva.Core` | Core 프레임워크 |
| Aveva.Core.Database.dll | `Aveva.Core.Database` | DbElement, DB 접근 |
| Aveva.Core.Database.Implementation.dll | — | DB 런타임 구현체 |
| Aveva.Core.Explorer.dll | `Aveva.Core.Explorer` | Element 탐색기 |
| Aveva.Core.Implementation.dll | — | Core 런타임 구현체 |
| Aveva.Core.Utilities.dll | `Aveva.Core.Utilities.CommandLine`, `Aveva.Core.Utilities.Messaging` | Command, PdmsMessage |
| Aveva.Core3D.Standalone.dll | `Aveva.Core3D.Shared` | 공유 타입 |
| Aveva.E3D.Implementation.dll | `Aveva.E3D.Implementation` | E3D 런타임 구현체 |
| Aveva.E3D.Standalone.dll | `Aveva.E3D.Standalone` | Standalone 클래스 |

## Workflow

```
1. Environment Setup  →  Hashtable에 환경변수 구성
2. Standalone.Start   →  E3D 엔진 초기화
3. Standalone.Open    →  프로젝트 로그인
4. Work               →  Command 실행 / DB 탐색
5. Standalone.Finish  →  엔진 종료
```

전체 연결 예제: [references/e3d-connection-template.cs](references/e3d-connection-template.cs)

### Step 1: Environment Setup

`Standalone.Start`에 전달할 환경변수 Hashtable 구성.

```csharp
var env = new Hashtable();

// 필수 환경변수
env.Add("AVEVA_DESIGN_EXE", @"C:\cae_prog\AVEVA\v2.x\e3d\");
env.Add("AVEVA_DESIGN_USER", @"<user_data_path>");
env.Add("AVEVA_DESIGN_WORK", @"<work_path>");
env.Add("AVEVA_PRODUCT", "E3D");
env.Add("projects_dir", @"<projects_root_path>");
env.Add("temp", Path.GetTempPath());
env.Add("PATH", @"C:\cae_prog\AVEVA\v2.x\e3d\;" + Environment.GetEnvironmentVariable("PATH"));
env.Add("PDMSBUF", @"<buffer_path>");
env.Add("PMLLIB", @"<pmllib_path>;C:\cae_prog\AVEVA\v2.x\e3d\");

// 프로젝트별 변수 (예: TESTPROJ)
env.Add("TESTPROJ000", @"J:\cae_proj\TESTPROJ\pdms\TESTPROJ000");
env.Add("TESTRPROJdflts", @"J:\cae_proj\TESTPROJ\pdms\TESTRPROJdflts");
```

XML config 파일에서 읽는 방식: [references/env-config-template.cs](references/env-config-template.cs)

### Step 2: Initialize

```csharp
// moduleNumber 78 = E3D Design 모듈
Standalone.Start(78, env);
```

### Step 3: Login

```csharp
PdmsMessage error;
if (!Standalone.Open(project, userId, password, mdb, out error))
{
    string errorMsg = error.MessageText();
    Standalone.ExitError(errorMsg);
    throw new Exception("E3D login failed: " + errorMsg);
}
```

### Step 4: Work

#### PML 명령 실행

```csharp
Command cmd = Command.CreateCommand("VAR !result FLNN");
if (cmd.Run())
{
    string result = cmd.Result.Trim();
}
else
{
    string errorMsg = cmd.Error.MessageText();
}
```

#### PML 매크로 파일 실행

```csharp
Command cmd = Command.CreateCommand("$M /path/to/macro.mac");
cmd.Run();
```

#### DB Element 접근

```csharp
DbElement world = DbElement.GetElement("/*");
bool isOpen = Project.CurrentProject.IsOpen();
```

### Step 5: Cleanup

```csharp
try { Standalone.Finish(); }
catch (Exception) { /* Finish may throw if already closed */ }
```

## Project Setup

### csproj 필수 설정

- **Target Framework**: .NET Framework 4.0 이상
- **Platform Target**: **x86** (AVEVA DLL은 32비트)
- **Output Type**: Exe 또는 WinExe

### csproj DLL 참조

```xml
<ItemGroup>
  <Reference Include="Aveva.Core">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core.Database">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.Database.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core.Database.Implementation">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.Database.Implementation.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core.Explorer">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.Explorer.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core.Implementation">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.Implementation.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core.Utilities">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core.Utilities.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.Core3D.Standalone">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.Core3D.Standalone.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.E3D.Implementation">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.E3D.Implementation.dll</HintPath>
  </Reference>
  <Reference Include="Aveva.E3D.Standalone">
    <HintPath>C:\cae_prog\AVEVA\v2.x\e3d\Aveva.E3D.Standalone.dll</HintPath>
  </Reference>
</ItemGroup>
```

## Common Patterns

### 다중 프로젝트 배치 처리

```csharp
foreach (string project in projectList)
{
    PdmsMessage error;
    if (Standalone.Open(project, user, pw, mdb, out error))
    {
        Command cmd = Command.CreateCommand(pmlScript);
        cmd.Run();
    }
}
```

### 매크로 파일 생성 후 실행

```csharp
string macroContent =
    "onerror continue" + Environment.NewLine +
    "VAR !result FLNN" + Environment.NewLine +
    "$P $!result";
string macroPath = Path.Combine(outputDir, "script.mac");
File.WriteAllText(macroPath, macroContent, Encoding.UTF8);

Command cmd = Command.CreateCommand("$M /" + macroPath);
cmd.Run();
```

## Runtime DLL Loading (필수)

AVEVA DLL은 앱 디렉토리가 아닌 E3D 설치 경로에 있으므로, `AssemblyResolve` 핸들러가 **반드시** 필요하다.
`Main` 진입 시 `Standalone.Start` 호출 전에 등록해야 한다.

```csharp
static string _e3dPath = @"C:\cae_prog\AVEVA\v2.x\e3d\";

static void Main(string[] args)
{
    AppDomain.CurrentDomain.AssemblyResolve += OnAssemblyResolve;
    // ... Standalone.Start, Open, etc.
}

static Assembly OnAssemblyResolve(object sender, ResolveEventArgs args)
{
    string assemblyName = new AssemblyName(args.Name).Name;
    string dllPath = Path.Combine(_e3dPath, assemblyName + ".dll");
    if (File.Exists(dllPath))
        return Assembly.LoadFrom(dllPath);
    return null;
}
```

이 핸들러 없이는 `DruidNet.dll` 등 간접 의존성 로드 시 `FileNotFoundException` 발생.

## 환경변수 로드 (evarProj.bat)

프로젝트별 환경변수는 `J:\cae_proj\evarProj.bat`으로 로드. 이 bat 파일은 각 프로젝트의 `evarProj_based.bat`를 호출하여 `{CODE}000`, `{CODE}MAC`, `{CODE}ISO`, `{CODE}PIC`, `{CODE}DFLTS` 경로와 RAS/GEV 카탈로그 경로를 설정한다.

**실행 bat 파일 패턴:**

```batch
@echo off
SET PATH=C:\cae_prog\AVEVA\v2.x\e3d\;%PATH%
call "J:\cae_proj\evarProj.bat"
MyApp.exe
```

C# 코드에서 `Environment.GetEnvironmentVariable()`로 읽어 Hashtable에 추가.

## Error Handling

| 상황 | 처리 |
|------|------|
| `Standalone.Open` returns false | `PdmsMessage` 읽기 → `Standalone.ExitError` → throw |
| `Command.Run()` returns false | `cmd.Error.MessageText()` 로그 후 판단 |
| `Standalone.Finish` throws | try-catch로 감싸기 (무시 가능) |
| DLL 로드 실패 | `AssemblyResolve` 핸들러 등록 확인, **x86** 플랫폼 타겟 확인 |

## References

- 접속 템플릿: [references/e3d-connection-template.cs](references/e3d-connection-template.cs)
- 환경변수 설정: [references/env-config-template.cs](references/env-config-template.cs)
- 참조 프로젝트: `refcode/e3dstandalone/`
