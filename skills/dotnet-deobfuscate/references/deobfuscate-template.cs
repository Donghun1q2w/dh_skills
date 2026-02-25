# deobfuscate-template.cs 참조 문서

## 전체 난독화 해제 스크립트

```csharp
// Program.cs - 난독화 해제기
// dotnet run -- <input.dll> [--output <output.dll>] [--detect-only]
using dnlib.DotNet;
using dnlib.DotNet.Emit;
using dnlib.DotNet.Writer;

string inputPath = "";
string? outputPath = null;
bool detectOnly = false;

for (int i = 0; i < args.Length; i++)
{
    switch (args[i])
    {
        case "--output" when i + 1 < args.Length:
            outputPath = args[++i]; break;
        case "--detect-only":
            detectOnly = true; break;
        default:
            if (!args[i].StartsWith("--")) inputPath = args[i]; break;
    }
}

if (string.IsNullOrEmpty(inputPath) || !File.Exists(inputPath))
{
    Console.Error.WriteLine("사용법: dotnet run -- <input.dll> [--output out.dll] [--detect-only]");
    return 1;
}

using var module = ModuleDefMD.Load(inputPath);

// ── 감지 전용 모드 ──
if (detectOnly)
{
    var (isObf, obfName) = DetectObfuscation(module);
    if (isObf)
    {
        Console.WriteLine($"⚠ 난독화 감지: {obfName}");
        Console.WriteLine($"  난독화된 이름 수: {CountObfuscatedNames(module)}");
    }
    else
        Console.WriteLine("✓ 난독화 감지되지 않음");
    return 0;
}

// ── 난독화 해제 실행 ──
outputPath ??= Path.Combine(
    Path.GetDirectoryName(inputPath)!,
    Path.GetFileNameWithoutExtension(inputPath) + "_cleaned" + Path.GetExtension(inputPath));

int renameCounter = 0;
int renamed = 0, decrypted = 0, attrsRemoved = 0, nopsRemoved = 0;

// 1. 이름 복원
Console.Error.WriteLine("[1/4] 이름 복원 중...");
var namespaceCounters = new Dictionary<string, int>();

foreach (var type in module.GetTypes())
{
    if (type.IsGlobalModuleType) continue;

    if (IsObfuscatedName(type.Name))
    {
        string kind = type.IsInterface ? "IFace" : type.IsEnum ? "Enum" :
                      type.IsValueType ? "Struct" : type.IsAbstract ? "Abstract" : "Class";
        string ns = string.IsNullOrEmpty(type.Namespace)
            ? "Global" : type.Namespace.Split('.').Last();
        if (!namespaceCounters.ContainsKey(ns)) namespaceCounters[ns] = 0;
        namespaceCounters[ns]++;
        type.Name = $"{kind}_{ns}_{namespaceCounters[ns]:D3}";
        renamed++;
    }

    foreach (var method in type.Methods)
    {
        if (method.IsConstructor || method.IsStaticConstructor) continue;
        if (IsObfuscatedName(method.Name))
        {
            string prefix = method.ReturnType.FullName switch
            {
                "System.Boolean" => "Check",
                "System.Void" => method.Parameters.Count <= 1 ? "Do" : "Process",
                "System.String" => "GetText",
                var rt when rt.StartsWith("System.Collections") => "GetList",
                _ => "Method"
            };
            method.Name = $"{prefix}_{renameCounter++:D4}";
            renamed++;
        }
    }

    foreach (var field in type.Fields)
    {
        if (IsObfuscatedName(field.Name))
        {
            string prefix = field.IsStatic ? "s_field" :
                field.FieldType.FullName switch
                {
                    "System.Boolean" => "m_flag",
                    "System.String" => "m_text",
                    "System.Int32" => "m_num",
                    _ => "m_field"
                };
            field.Name = $"{prefix}_{renameCounter++:D4}";
            renamed++;
        }
    }

    foreach (var prop in type.Properties)
    {
        if (IsObfuscatedName(prop.Name))
        {
            prop.Name = $"Prop_{renameCounter++:D4}";
            renamed++;
        }
    }
}

// 2. 문자열 복호화 (Base64)
Console.Error.WriteLine("[2/4] 문자열 복호화 중...");
foreach (var type in module.GetTypes())
{
    foreach (var method in type.Methods)
    {
        if (!method.HasBody) continue;
        var instrs = method.Body.Instructions;
        for (int i = 0; i < instrs.Count - 1; i++)
        {
            if (instrs[i].OpCode == OpCodes.Ldstr &&
                instrs[i + 1].OpCode == OpCodes.Call &&
                instrs[i + 1].Operand is MethodDef calledMethod &&
                IsBase64DecodeMethod(calledMethod))
            {
                try
                {
                    string encoded = (string)instrs[i].Operand;
                    byte[] bytes = Convert.FromBase64String(encoded);
                    instrs[i].Operand = System.Text.Encoding.UTF8.GetString(bytes);
                    instrs[i + 1].OpCode = OpCodes.Nop;
                    decrypted++;
                }
                catch { }
            }
        }
    }
}

// 3. 어트리뷰트 제거
Console.Error.WriteLine("[3/4] 난독화 어트리뷰트 제거 중...");
var keywords = new[] { "Dotfuscator", "Obfusc", "ConfusedBy", "SmartAssembly",
    "Suppress", "NETGuard", "Babel", "Eazfuscator", "CryptoObfuscator", "ILProtector" };

attrsRemoved += RemoveAttrs(module.CustomAttributes, keywords);
if (module.Assembly != null)
    attrsRemoved += RemoveAttrs(module.Assembly.CustomAttributes, keywords);
foreach (var t in module.GetTypes())
    attrsRemoved += RemoveAttrs(t.CustomAttributes, keywords);

// 4. NOP 정리
Console.Error.WriteLine("[4/4] 데드코드 정리 중...");
foreach (var type in module.GetTypes())
{
    foreach (var method in type.Methods)
    {
        if (!method.HasBody) continue;
        var instrs = method.Body.Instructions;
        for (int i = instrs.Count - 1; i >= 0; i--)
        {
            if (instrs[i].OpCode == OpCodes.Nop &&
                !instrs.Any(x => x.Operand == instrs[i]))
            {
                instrs.RemoveAt(i);
                nopsRemoved++;
            }
        }
    }
}

// 저장
Console.Error.WriteLine("[저장] 정리된 어셈블리 저장 중...");
var writerOptions = new ModuleWriterOptions(module) { Logger = DummyLogger.NoThrowInstance };
module.Write(outputPath, writerOptions);

// 결과 출력
Console.WriteLine("=== 난독화 해제 결과 ===");
Console.WriteLine($"이름 복원:      {renamed}");
Console.WriteLine($"문자열 복호화:  {decrypted}");
Console.WriteLine($"어트리뷰트 제거: {attrsRemoved}");
Console.WriteLine($"데드코드 정리:  {nopsRemoved}");
Console.WriteLine($"합계:           {renamed + decrypted + attrsRemoved + nopsRemoved}");
Console.WriteLine($"출력:           {outputPath}");
return 0;

// ── 헬퍼 메서드 ──
static bool IsObfuscatedName(string name)
{
    if (string.IsNullOrEmpty(name)) return false;
    if (name.StartsWith("<") || name.StartsWith("__")) return false;
    if (name.StartsWith("get_") || name.StartsWith("set_") ||
        name == ".ctor" || name == ".cctor") return false;
    if (name.Any(c => char.IsControl(c) && c != '\t' && c != '\n' && c != '\r')) return true;
    if (name.Length == 1 && char.IsLetter(name[0])) return true;
    if (name.Any(c => c > 0x7F && !char.IsLetterOrDigit(c))) return true;
    if (name.Length > 15 && name.All(c => char.IsLetterOrDigit(c) || c == '_'))
    {
        int vowels = name.Count(c => "aeiouAEIOU".Contains(c));
        if ((double)vowels / name.Length < 0.1) return true;
    }
    return false;
}

static (bool, string?) DetectObfuscation(ModuleDefMD module)
{
    var map = new Dictionary<string, string>
    {
        {"Dotfuscator","Dotfuscator"}, {"ConfusedBy","ConfuserEx"},
        {"SmartAssembly","SmartAssembly"}, {"Eazfuscator","Eazfuscator.NET"},
    };
    var attrs = module.CustomAttributes
        .Concat(module.Assembly?.CustomAttributes ?? Enumerable.Empty<CustomAttribute>());
    foreach (var a in attrs)
        foreach (var (k,v) in map)
            if (a.TypeFullName.Contains(k, StringComparison.OrdinalIgnoreCase))
                return (true, v);

    int obf = CountObfuscatedNames(module);
    int total = module.GetTypes().Count() + module.GetTypes().Sum(t => t.Methods.Count);
    if (total > 0 && (double)obf / total > 0.3) return (true, "Unknown");
    return (false, null);
}

static int CountObfuscatedNames(ModuleDefMD module)
{
    int count = 0;
    foreach (var t in module.GetTypes())
    {
        if (IsObfuscatedName(t.Name)) count++;
        foreach (var m in t.Methods)
            if (IsObfuscatedName(m.Name)) count++;
    }
    return count;
}

static bool IsBase64DecodeMethod(MethodDef method)
{
    if (!method.HasBody) return false;
    return method.Body.Instructions.Any(i =>
        i.OpCode == OpCodes.Call && i.Operand is IMethodDefOrRef mr && mr.Name == "FromBase64String");
}

static int RemoveAttrs(CustomAttributeCollection attrs, string[] keywords)
{
    int c = 0;
    for (int i = attrs.Count - 1; i >= 0; i--)
        if (keywords.Any(k => attrs[i].TypeFullName.Contains(k, StringComparison.OrdinalIgnoreCase)))
        { attrs.RemoveAt(i); c++; }
    return c;
}
```
