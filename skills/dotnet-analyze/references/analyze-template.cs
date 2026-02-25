# analyze-template.cs 참조 문서

이 문서는 `dotnet-analyze` 스킬이 어셈블리 분석 시 생성하는 C# 스크립트의 전체 템플릿이다.
Claude는 이 템플릿을 기반으로 분석 스크립트를 작성하되, 사용자 요청에 맞게 수정할 수 있다.

## 전체 분석 스크립트 템플릿

```csharp
// Program.cs - 어셈블리 구조 분석기
// 대상 파일 경로를 인자로 받는다: dotnet run -- "path/to/target.dll"
using dnlib.DotNet;
using dnlib.DotNet.Emit;
using System.Text.Json;

if (args.Length == 0)
{
    Console.Error.WriteLine("사용법: dotnet run -- <assembly-path>");
    return 1;
}

string targetPath = args[0];
if (!File.Exists(targetPath))
{
    Console.Error.WriteLine($"파일 없음: {targetPath}");
    return 1;
}

using var module = ModuleDefMD.Load(targetPath);

// ── 기본 정보 ──
Console.WriteLine("=== 어셈블리 기본 정보 ===");
Console.WriteLine($"이름: {module.Assembly?.FullName ?? module.Name}");
Console.WriteLine($"런타임: {module.RuntimeVersion}");
Console.WriteLine($"엔트리포인트: {module.EntryPoint?.FullName ?? "없음"}");

// ── 참조 어셈블리 ──
Console.WriteLine("\n=== 참조 어셈블리 ===");
foreach (var asmRef in module.GetAssemblyRefs())
    Console.WriteLine($"  {asmRef.Name} v{asmRef.Version}");

// ── 리소스 ──
Console.WriteLine($"\n=== 임베디드 리소스 ({module.Resources.Count}개) ===");
foreach (var res in module.Resources)
    Console.WriteLine($"  {res.Name}");

// ── 타입 분석 ──
var allTypes = module.GetTypes()
    .Where(t => !t.IsGlobalModuleType && !t.Name.StartsWith("<"))
    .ToList();

var namespaces = allTypes.Select(t => t.Namespace?.ToString() ?? "(Global)")
    .Distinct().OrderBy(n => n).ToList();

Console.WriteLine($"\n=== 타입 통계 ===");
Console.WriteLine($"네임스페이스: {namespaces.Count}");
Console.WriteLine($"전체 타입: {allTypes.Count}");
Console.WriteLine($"  클래스: {allTypes.Count(t => t.IsClass && !t.IsEnum && !t.IsValueType && !t.IsInterface)}");
Console.WriteLine($"  인터페이스: {allTypes.Count(t => t.IsInterface)}");
Console.WriteLine($"  열거형: {allTypes.Count(t => t.IsEnum)}");
Console.WriteLine($"  구조체: {allTypes.Count(t => t.IsValueType && !t.IsEnum)}");
Console.WriteLine($"전체 메서드: {allTypes.Sum(t => t.Methods.Count)}");
Console.WriteLine($"전체 프로퍼티: {allTypes.Sum(t => t.Properties.Count)}");
Console.WriteLine($"전체 필드: {allTypes.Sum(t => t.Fields.Count)}");

// ── 난독화 감지 ──
Console.WriteLine("\n=== 난독화 감지 ===");

// 어트리뷰트 기반 감지
var obfuscatorKeywords = new Dictionary<string, string>
{
    {"Dotfuscator", "Dotfuscator"}, {"ConfusedBy", "ConfuserEx"},
    {"SmartAssembly", "SmartAssembly"}, {"Eazfuscator", "Eazfuscator.NET"},
    {"Babel", "Babel"}, {"CryptoObfuscator", "Crypto Obfuscator"},
    {"NETGuard", ".NET Guard"}, {"ILProtector", "ILProtector"},
    {"DeepSea", "DeepSea"}, {"Agile", "Agile.NET"}, {"Xenocode", "Xenocode"},
};

string? detectedObfuscator = null;
var allAttrs = module.CustomAttributes
    .Concat(module.Assembly?.CustomAttributes ?? Enumerable.Empty<CustomAttribute>());

foreach (var attr in allAttrs)
{
    foreach (var (key, name) in obfuscatorKeywords)
    {
        if (attr.TypeFullName.Contains(key, StringComparison.OrdinalIgnoreCase))
        {
            detectedObfuscator = name;
            break;
        }
    }
    if (detectedObfuscator != null) break;
}

// 이름 패턴 기반 휴리스틱
int obfuscatedNames = 0, totalNames = 0;
foreach (var t in allTypes)
{
    totalNames++;
    if (IsObfuscatedName(t.Name)) obfuscatedNames++;
    foreach (var m in t.Methods)
    {
        totalNames++;
        if (IsObfuscatedName(m.Name)) obfuscatedNames++;
    }
}

double ratio = totalNames > 0 ? (double)obfuscatedNames / totalNames : 0;

if (detectedObfuscator != null)
    Console.WriteLine($"감지됨: {detectedObfuscator} (어트리뷰트 확인)");
else if (ratio > 0.3)
{
    bool hasControlChars = allTypes.Any(t =>
        t.Name.Any(c => char.IsControl(c) && c != '\t' && c != '\n'));
    string guess = hasControlChars ? "ConfuserEx (추정)" : "알 수 없는 도구";
    Console.WriteLine($"감지됨: {guess} (이름 {ratio:P0} 난독화)");
}
else
    Console.WriteLine("감지 안됨");

Console.WriteLine($"난독화된 이름: {obfuscatedNames}/{totalNames}");

// ── 타입 구조 트리 ──
Console.WriteLine("\n=== 타입 구조 ===");
foreach (var ns in namespaces)
{
    Console.WriteLine($"\n📁 {ns}");
    var nsTypes = allTypes.Where(t => (t.Namespace?.ToString() ?? "(Global)") == ns);
    foreach (var type in nsTypes.OrderBy(t => t.Name))
    {
        string icon = type.IsInterface ? "🔷" : type.IsEnum ? "🔶" :
                       type.IsValueType ? "🔸" : "📦";
        string kind = type.IsInterface ? "Interface" : type.IsEnum ? "Enum" :
                       type.IsValueType ? "Struct" : "Class";
        Console.WriteLine($"  {icon} {type.Name} ({kind})");

        foreach (var method in type.Methods.Where(m => !m.Name.StartsWith("<")).Take(10))
        {
            string access = method.IsPublic ? "public" : method.IsPrivate ? "private" :
                            method.IsFamily ? "protected" : "internal";
            string parms = string.Join(", ", method.Parameters
                .Where(p => !p.IsHiddenThisParameter)
                .Select(p => $"{p.Type?.FullName?.Split('.').Last() ?? "?"} {p.Name}"));
            Console.WriteLine($"    🔧 {access} {method.ReturnType?.FullName?.Split('.').Last()} {method.Name}({parms})");
        }
        if (type.Methods.Count(m => !m.Name.StartsWith("<")) > 10)
            Console.WriteLine($"    ... +{type.Methods.Count(m => !m.Name.StartsWith("<")) - 10} more");
    }
}

return 0;

// ── 헬퍼 ──
static bool IsObfuscatedName(string name)
{
    if (string.IsNullOrEmpty(name)) return false;
    if (name.StartsWith("<") || name.StartsWith("__")) return false;
    if (name.StartsWith("get_") || name.StartsWith("set_") ||
        name.StartsWith("add_") || name.StartsWith("remove_") ||
        name == ".ctor" || name == ".cctor") return false;

    if (name.Any(c => char.IsControl(c) && c != '\t' && c != '\n' && c != '\r'))
        return true;
    if (name.Length == 1 && char.IsLetter(name[0])) return true;
    if (name.Any(c => c > 0x7F && !char.IsLetterOrDigit(c))) return true;
    if (name.Length > 15 && name.All(c => char.IsLetterOrDigit(c) || c == '_'))
    {
        int vowels = name.Count(c => "aeiouAEIOU".Contains(c));
        if ((double)vowels / name.Length < 0.1) return true;
    }
    return false;
}
```

## 사용법

```bash
cd /tmp/dotnet-analyzer
# Program.cs에 위 코드를 작성한 후
dotnet run -- "C:\path\to\target.dll"
```

## JSON 출력 변형

사용자가 JSON 내보내기를 요청하면, 마지막에 다음을 추가한다:

```csharp
// JSON 출력
var jsonResult = new
{
    Assembly = module.Assembly?.FullName,
    Runtime = module.RuntimeVersion,
    References = module.GetAssemblyRefs().Select(r => $"{r.Name} v{r.Version}").ToList(),
    Statistics = new { Namespaces = namespaces.Count, Types = allTypes.Count, /* ... */ },
    IsObfuscated = detectedObfuscator != null || ratio > 0.3,
    ObfuscatorName = detectedObfuscator,
    Types = allTypes.Select(t => new { t.FullName, Kind = /* ... */ }).ToList()
};
string json = JsonSerializer.Serialize(jsonResult, new JsonSerializerOptions { WriteIndented = true });
File.WriteAllText("analysis_result.json", json);
Console.WriteLine($"\nJSON 저장: analysis_result.json");
```
