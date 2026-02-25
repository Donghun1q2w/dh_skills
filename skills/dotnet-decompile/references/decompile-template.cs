# decompile-template.cs 참조 문서

## 전체 디컴파일 스크립트

```csharp
// Program.cs - 디컴파일러
// dotnet run -- <assembly-path> [--type <FullTypeName>] [--output <dir>] [--single-file]
using ICSharpCode.Decompiler;
using ICSharpCode.Decompiler.CSharp;
using ICSharpCode.Decompiler.TypeSystem;

string targetPath = "";
string? typeName = null;
string? outputDir = null;
bool singleFile = false;

// 인자 파싱
for (int i = 0; i < args.Length; i++)
{
    switch (args[i])
    {
        case "--type" when i + 1 < args.Length:
            typeName = args[++i]; break;
        case "--output" when i + 1 < args.Length:
            outputDir = args[++i]; break;
        case "--single-file":
            singleFile = true; break;
        default:
            if (!args[i].StartsWith("--")) targetPath = args[i]; break;
    }
}

if (string.IsNullOrEmpty(targetPath) || !File.Exists(targetPath))
{
    Console.Error.WriteLine("사용법: dotnet run -- <assembly.dll> [--type Name] [--output dir] [--single-file]");
    return 1;
}

var settings = new DecompilerSettings(LanguageVersion.CSharp11)
{
    ThrowOnAssemblyResolveErrors = false,
    ShowXmlDocumentation = true,
    RemoveDeadCode = true,
    RemoveDeadStores = true,
};

var decompiler = new CSharpDecompiler(targetPath, settings);

// ── 특정 타입 디컴파일 ──
if (!string.IsNullOrEmpty(typeName))
{
    Console.Error.WriteLine($"[디컴파일] 타입: {typeName}");
    try
    {
        string source = decompiler.DecompileTypeAsString(new FullTypeName(typeName));
        if (outputDir != null)
        {
            Directory.CreateDirectory(outputDir);
            string outFile = Path.Combine(outputDir, typeName.Split('.').Last() + ".cs");
            File.WriteAllText(outFile, source);
            Console.Error.WriteLine($"[저장] {outFile}");
        }
        else
        {
            Console.WriteLine(source);
        }
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine($"[오류] {ex.Message}");
        return 1;
    }
    return 0;
}

// ── 전체 디컴파일: 단일 파일 ──
if (singleFile)
{
    Console.Error.WriteLine("[디컴파일] 전체 → 단일 파일");
    string fullSource = decompiler.DecompileWholeModuleAsString();
    string outFile = Path.Combine(
        outputDir ?? ".",
        Path.GetFileNameWithoutExtension(targetPath) + "_decompiled.cs");
    Directory.CreateDirectory(Path.GetDirectoryName(outFile)!);
    File.WriteAllText(outFile, fullSource);
    Console.Error.WriteLine($"[저장] {outFile} ({new FileInfo(outFile).Length / 1024}KB)");
    return 0;
}

// ── 전체 디컴파일: 타입별 개별 파일 ──
string outDir = outputDir ?? Path.GetFileNameWithoutExtension(targetPath) + "_src";
Directory.CreateDirectory(outDir);

var types = decompiler.TypeSystem.GetAllTypeDefinitions()
    .Where(t => !t.Name.StartsWith("<"))
    .ToList();

Console.Error.WriteLine($"[디컴파일] {types.Count}개 타입 → {outDir}/");

int success = 0, failed = 0;

foreach (var type in types)
{
    try
    {
        string source = decompiler.DecompileTypeAsString(new FullTypeName(type.FullName));

        string[] parts = type.FullName.Split('.');
        string fileName = SanitizeFileName(parts.Last()) + ".cs";
        string subDir = parts.Length > 1
            ? Path.Combine(parts.Take(parts.Length - 1).ToArray())
            : "";

        string dir = Path.Combine(outDir, subDir);
        Directory.CreateDirectory(dir);
        File.WriteAllText(Path.Combine(dir, fileName), source);
        success++;
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine($"  [실패] {type.FullName}: {ex.Message}");
        failed++;
    }
}

Console.Error.WriteLine($"[완료] 성공: {success}, 실패: {failed}");
return 0;

static string SanitizeFileName(string name)
{
    foreach (char c in Path.GetInvalidFileNameChars())
        name = name.Replace(c, '_');
    return name;
}
```

## 파워 유저 팁

### 특정 네임스페이스만 디컴파일

```csharp
var types = decompiler.TypeSystem.GetAllTypeDefinitions()
    .Where(t => !t.Name.StartsWith("<"))
    .Where(t => t.Namespace.StartsWith("MyApp.Services"));
```

### 메서드 수준 디컴파일

```csharp
// 특정 메서드만 디컴파일하려면 ILSpy의 method handle을 사용
var typeDef = decompiler.TypeSystem.FindType(new FullTypeName("MyApp.Program"))
    as ITypeDefinition;
var method = typeDef?.Methods.First(m => m.Name == "Main");
// 현재 ICSharpCode.Decompiler API는 타입 단위가 최소 단위
// 메서드만 필요하면 타입을 디컴파일한 후 텍스트에서 추출
```

### 디컴파일 품질 향상

PDB 파일이 있으면 변수 이름과 줄 번호가 복원된다:
```csharp
// PDB가 같은 디렉토리에 있으면 자동으로 로드됨
// target.dll + target.pdb → 원본에 가까운 결과
```
