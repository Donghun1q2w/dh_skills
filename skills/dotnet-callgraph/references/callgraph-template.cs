# callgraph-template.cs 참조 문서

## 전체 호출 관계 분석 스크립트

```csharp
// Program.cs - 호출 관계 분석기
// dotnet run -- <assembly.dll> [--namespace <ns>] [--format mermaid|dot|console] [--output <file>] [--max-nodes <N>]
using dnlib.DotNet;
using dnlib.DotNet.Emit;
using System.Text;

string targetPath = "";
string? nsFilter = null;
string format = "mermaid";
string? outputFile = null;
int maxNodes = 50;

for (int i = 0; i < args.Length; i++)
{
    switch (args[i])
    {
        case "--namespace" when i + 1 < args.Length: nsFilter = args[++i]; break;
        case "--format" when i + 1 < args.Length: format = args[++i]; break;
        case "--output" when i + 1 < args.Length: outputFile = args[++i]; break;
        case "--max-nodes" when i + 1 < args.Length: maxNodes = int.Parse(args[++i]); break;
        default:
            if (!args[i].StartsWith("--")) targetPath = args[i]; break;
    }
}

if (string.IsNullOrEmpty(targetPath) || !File.Exists(targetPath))
{
    Console.Error.WriteLine("사용법: dotnet run -- <assembly.dll> [--namespace ns] [--format mermaid|dot|console] [--max-nodes 50]");
    return 1;
}

using var module = ModuleDefMD.Load(targetPath);

// ── 호출 관계 수집 ──
Console.Error.WriteLine("[분석] 호출 관계 수집 중...");
var graph = new Dictionary<string, (string FullName, List<string> Calls, List<string> CalledBy)>();

void EnsureNode(string name, string fullName = "")
{
    if (!graph.ContainsKey(name))
        graph[name] = (fullName, new List<string>(), new List<string>());
}

foreach (var type in module.GetTypes())
{
    if (type.IsGlobalModuleType || type.Name.StartsWith("<")) continue;
    if (nsFilter != null && !(type.Namespace?.Contains(nsFilter) ?? false)) continue;

    foreach (var method in type.Methods.Where(m => m.HasBody))
    {
        string caller = $"{type.Name}.{method.Name}";
        EnsureNode(caller, $"{type.FullName}.{method.Name}");

        foreach (var instr in method.Body.Instructions)
        {
            if (instr.OpCode != OpCodes.Call &&
                instr.OpCode != OpCodes.Callvirt &&
                instr.OpCode != OpCodes.Newobj) continue;

            if (instr.Operand is not IMethodDefOrRef calledMethod) continue;

            // System/Microsoft 내부 호출 제외
            string? declNs = calledMethod.DeclaringType?.Namespace;
            if (declNs != null && (declNs.StartsWith("System") || declNs.StartsWith("Microsoft")))
                continue;

            string callee = $"{calledMethod.DeclaringType?.Name ?? "?"}.{calledMethod.Name}";
            EnsureNode(callee, $"{calledMethod.DeclaringType?.FullName ?? "?"}.{calledMethod.Name}");

            if (!graph[caller].Calls.Contains(callee))
                graph[caller].Calls.Add(callee);
            if (!graph[callee].CalledBy.Contains(caller))
                graph[callee].CalledBy.Add(caller);
        }
    }
}

Console.Error.WriteLine($"[결과] {graph.Count}개 노드, {graph.Sum(g => g.Value.Calls.Count)}개 연결");

if (graph.Count == 0)
{
    Console.Error.WriteLine("⚠ 호출 관계가 발견되지 않았습니다.");
    return 0;
}

// ── 상위 노드 선택 ──
var topNodes = graph
    .OrderByDescending(g => g.Value.CalledBy.Count + g.Value.Calls.Count)
    .Take(maxNodes)
    .ToDictionary(g => g.Key, g => g.Value);

var topNames = new HashSet<string>(topNodes.Keys);

// ── 출력 ──
switch (format.ToLower())
{
    case "mermaid":
    {
        var sb = new StringBuilder();
        sb.AppendLine("graph TD");
        int idCounter = 0;
        var idMap = new Dictionary<string, string>();
        string GetId(string name) {
            if (!idMap.ContainsKey(name)) idMap[name] = $"N{idCounter++}";
            return idMap[name];
        }

        foreach (var (name, data) in topNodes)
        {
            foreach (var called in data.Calls.Where(c => topNames.Contains(c)))
            {
                sb.AppendLine($"    {GetId(name)}[\"{Esc(name)}\"] --> {GetId(called)}[\"{Esc(called)}\"]");
            }
        }

        string content = sb.ToString();
        if (outputFile != null)
        {
            File.WriteAllText(outputFile, content);
            Console.Error.WriteLine($"[저장] {outputFile}");
            Console.Error.WriteLine("💡 https://mermaid.live 에서 렌더링 가능");
        }
        else Console.WriteLine(content);
        break;
    }

    case "dot":
    case "graphviz":
    {
        var sb = new StringBuilder();
        sb.AppendLine("digraph CallGraph {");
        sb.AppendLine("    rankdir=LR;");
        sb.AppendLine("    node [shape=box, style=filled, fillcolor=lightblue, fontname=\"Consolas\", fontsize=10];");
        sb.AppendLine("    edge [color=gray60];");
        sb.AppendLine();

        // 핫 노드 강조
        foreach (var (name, data) in topNodes.Where(n => n.Value.CalledBy.Count >= 5))
            sb.AppendLine($"    \"{EscDot(name)}\" [fillcolor=orange, style=\"filled,bold\"];");

        // God 메서드 강조
        foreach (var (name, data) in topNodes.Where(n => n.Value.Calls.Count >= 10))
            sb.AppendLine($"    \"{EscDot(name)}\" [fillcolor=red, fontcolor=white, style=\"filled,bold\"];");

        sb.AppendLine();
        foreach (var (name, data) in topNodes)
            foreach (var called in data.Calls.Where(c => topNames.Contains(c)))
                sb.AppendLine($"    \"{EscDot(name)}\" -> \"{EscDot(called)}\";");

        sb.AppendLine("}");

        string content = sb.ToString();
        if (outputFile != null)
        {
            File.WriteAllText(outputFile, content);
            Console.Error.WriteLine($"[저장] {outputFile}");
            Console.Error.WriteLine("💡 렌더링: dot -Tpng graph.dot -o graph.png");
        }
        else Console.WriteLine(content);
        break;
    }

    default: // console
    {
        // Top 호출받는 메서드
        Console.WriteLine("\n=== 가장 많이 호출되는 메서드 (Top 20) ===");
        Console.WriteLine($"{"메서드",-40} {"호출 횟수",8}  호출원");
        Console.WriteLine(new string('-', 90));
        foreach (var (name, data) in topNodes
            .OrderByDescending(n => n.Value.CalledBy.Count)
            .Take(20)
            .Where(n => n.Value.CalledBy.Count > 0))
        {
            string callers = string.Join(", ", data.CalledBy.Take(3));
            if (data.CalledBy.Count > 3) callers += $" +{data.CalledBy.Count - 3}";
            Console.WriteLine($"{name,-40} {data.CalledBy.Count,8}  {callers}");
        }

        // Top 호출하는 메서드
        Console.WriteLine("\n=== 가장 많은 호출을 하는 메서드 (Top 20) ===");
        Console.WriteLine($"{"메서드",-40} {"호출 수",8}  호출 대상");
        Console.WriteLine(new string('-', 90));
        foreach (var (name, data) in topNodes
            .OrderByDescending(n => n.Value.Calls.Count)
            .Take(20)
            .Where(n => n.Value.Calls.Count > 0))
        {
            string calls = string.Join(", ", data.Calls.Take(3));
            if (data.Calls.Count > 3) calls += $" +{data.Calls.Count - 3}";
            Console.WriteLine($"{name,-40} {data.Calls.Count,8}  {calls}");
        }

        // 순환 참조 감지
        Console.WriteLine("\n=== 순환 참조 감지 ===");
        int cycles = 0;
        foreach (var (name, data) in topNodes)
        {
            foreach (var called in data.Calls)
            {
                if (graph.ContainsKey(called) && graph[called].Calls.Contains(name))
                {
                    Console.WriteLine($"  ⚠ {name} ↔ {called}");
                    cycles++;
                }
            }
        }
        if (cycles == 0) Console.WriteLine("  ✓ 순환 참조 없음");
        break;
    }
}

return 0;

static string Esc(string s) => s.Replace("\"", "&quot;").Replace("<", "&lt;").Replace(">", "&gt;");
static string EscDot(string s) => s.Replace("\"", "\\\"");
```

## 사용 예시

```bash
cd /tmp/dotnet-analyzer

# Mermaid 다이어그램 (파일 저장)
dotnet run -- "C:\path\to\app.dll" --format mermaid --output callgraph.mermaid

# DOT 다이어그램 → PNG
dotnet run -- "C:\path\to\app.dll" --format dot --output callgraph.dot
dot -Tpng callgraph.dot -o callgraph.png

# 콘솔 테이블 (특정 네임스페이스)
dotnet run -- "C:\path\to\app.dll" --format console --namespace "MyApp.Services"

# 대규모 분석 (노드 확장)
dotnet run -- "C:\path\to\app.dll" --max-nodes 200 --format dot --output full_graph.dot
```
