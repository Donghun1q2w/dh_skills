---
name: dotnet-decompile
description: "Decompiles .NET assemblies (DLL/EXE) into C# source code. Recovers IL code into near-original C# code and saves to files. Must be used for requests like 'recover source code', 'decompile', 'convert to C# code', 'extract code from DLL', 'get me the source', or 'show me the code'. Also supports extracting specific classes or saving the entire assembly as separate .cs files organized by namespace."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET Assembly Decompilation (IL → C#)

Uses ICSharpCode.Decompiler (ILSpy engine) to recover .NET assemblies into C# source code.

## Prerequisites

- .NET 8 SDK
- Shared project setup: Run `scripts/setup-project.sh` from the `dotnet-analyze` skill first

## Decompilation Modes

### Mode 1: Entire Assembly → Single File

Outputs the entire target assembly as a single .cs file. Suitable for quick inspection.

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

### Mode 2: Individual .cs Files Per Type

Maps namespaces to directory structures and saves each type as an individual .cs file. Most useful for code analysis.

```csharp
var types = decompiler.TypeSystem.GetAllTypeDefinitions()
    .Where(t => !t.Name.StartsWith("<"));

foreach (var type in types)
{
    string source = decompiler.DecompileTypeAsString(new FullTypeName(type.FullName));

    // Namespace → Directory
    string[] parts = type.FullName.Split('.');
    string dir = Path.Combine(outputDir, Path.Combine(parts.Take(parts.Length - 1).ToArray()));
    Directory.CreateDirectory(dir);

    string filePath = Path.Combine(dir, SanitizeFileName(parts.Last()) + ".cs");
    File.WriteAllText(filePath, source);
}
```

### Mode 3: Decompile Specific Type Only

When the user specifies a particular class/interface.

```csharp
string source = decompiler.DecompileTypeAsString(new FullTypeName("MyApp.Services.UserService"));
Console.WriteLine(source);
```

## Full Script Template

See `references/decompile-template.cs` for the detailed template.

## Output Structure Example

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

## DecompilerSettings Key Options

| Option | Default | Description |
|--------|---------|-------------|
| `LanguageVersion` | CSharp11 | Output C# version (uses latest syntax) |
| `ThrowOnAssemblyResolveErrors` | false | Suppress exceptions on reference resolution failure |
| `RemoveDeadCode` | true | Remove unused code |
| `RemoveDeadStores` | true | Remove unnecessary variable assignments |
| `ShowXmlDocumentation` | true | Include XML doc comments |
| `DecompileMemberBodies` | true | Decompile method bodies |

## Decompilation Failure Handling

Some types may fail to decompile. Failed types are skipped and recorded as comments:

```csharp
try
{
    string source = decompiler.DecompileTypeAsString(new FullTypeName(type.FullName));
    // Save
}
catch (Exception ex)
{
    string fallback = $"// Decompilation failed: {type.FullName}\n// Error: {ex.Message}\n";
    // Save fallback
}
```

## Handling Obfuscated Assemblies

For assemblies where obfuscation is detected, it is recommended to clean them first using the `dotnet-deobfuscate` skill before decompilation. Decompiling in an obfuscated state will produce unreadable variable names and control flow as-is.

## Notes

- Decompiled code is not 100% identical to the original (due to compiler optimizations, debug info loss)
- `async/await`, LINQ, etc. may appear as state machines
- Full decompilation of large assemblies (500+ types) may take several minutes
