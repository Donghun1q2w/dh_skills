---
name: dotnet-analyze
description: "Entry point for .NET assembly (DLL/EXE) analysis. Performs structure analysis, metadata extraction, obfuscation detection, and referenced assembly inspection. Use when the user requests DLL analysis, EXE reversing, .NET binary structure inspection, assembly info lookup, or type/class/method listing. Must be used for requests like 'analyze this DLL', 'figure out what this EXE does', 'show me the .NET assembly structure', or 'list all classes'."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET Assembly Structure Analysis

A skill for analyzing metadata, type structures, references, and obfuscation status of .NET DLL/EXE files.

## Prerequisites

- .NET 8 SDK required (verify with `dotnet --version`)
- Target: .NET managed code assemblies (DLL or EXE)

## Analysis Workflow

### Step 1: Environment Check & Project Setup

```bash
# Check .NET SDK
dotnet --version

# Create temporary analysis project if it doesn't exist
if [ ! -f "/tmp/dotnet-analyzer/DotNetAnalyzer.csproj" ]; then
  mkdir -p /tmp/dotnet-analyzer
  # Run scripts/setup-project.sh to initialize the project
fi
```

If the project doesn't exist, run `scripts/setup-project.sh` to create a C# console project with NuGet packages (ICSharpCode.Decompiler, dnlib, Spectre.Console).

### Step 2: Extract Assembly Basic Information

Generate and execute the following C# script. The full template is available in `references/analyze-template.cs`.

Key analysis items:
- **Assembly name** and version
- **Target framework** (.NET Framework / .NET Core / .NET 5+)
- **Runtime version**
- **Type counts** (classes, interfaces, enums, structs, delegates)
- **Method/property/field counts**
- **Referenced assemblies** list
- **Embedded resources** list
- **Obfuscation detection** (known tool signatures + heuristics)

### Step 3: Type Structure Tree Output

Organize the namespace → type → member hierarchy in a tree format.

```
📦 MyApp.Services
  📦 UserService (Class)
    🔧 public Task<User> GetUserAsync(int id)
    🔧 public void UpdateUser(User user)
    🔹 private readonly IDbContext _db
  🔷 IUserRepository (Interface)
    🔧 Task<User> FindById(int id)
```

### Step 4: Result Analysis & Follow-up Suggestions

Suggest appropriate follow-up skills based on the analysis results:

| Scenario | Follow-up Skill |
|----------|----------------|
| Want to recover source code | Use `dotnet-decompile` skill |
| Obfuscation detected | Use `dotnet-deobfuscate` skill |
| Want to understand call relationships | Use `dotnet-callgraph` skill |

## Obfuscation Detection Criteria

The following patterns are used to determine obfuscation:

**Attribute-based** (definitive):
- `Dotfuscator`, `ConfusedBy`, `SmartAssembly`, `Eazfuscator`, `Babel`, `CryptoObfuscator`, `NETGuard`, `ILProtector`, `DeepSea`, `Agile`, `Xenocode`

**Name pattern-based** (heuristic):
- Contains Unicode control characters → suspected ConfuserEx
- Many single-character names (a, b, c...)
- Non-ASCII character patterns
- Long names with less than 10% vowel ratio (Base64-like)
- Classified as "obfuscated" if 30% or more of all names match the above patterns

## Output Format

Analysis results are displayed as a structured table:

```
┌──────────────────────────────────────┐
│      Assembly Analysis Summary       │
├─────────────────┬────────────────────┤
│ Assembly        │ MyApp v1.2.3       │
│ Framework       │ .NET 8.0           │
│ Types           │ 47                 │
│ Methods         │ 312                │
│ References      │ 12                 │
│ Obfuscation     │ No                 │
└─────────────────┴────────────────────┘
```

JSON export is also supported (on user request).

## Notes

- Native C++ DLLs and mixed-mode assemblies cannot be fully analyzed
- Some metadata reading may fail for .NET Framework 1.x assemblies
- Large assemblies (1000+ types) may take tens of seconds to analyze
