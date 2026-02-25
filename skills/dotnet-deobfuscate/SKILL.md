---
name: dotnet-deobfuscate
description: "Cleans obfuscated .NET assemblies. Performs unreadable name restoration, encrypted string decryption, obfuscation attribute removal, and dead code cleanup to produce a clean, analyzable DLL/EXE. Must be used for requests like 'deobfuscate', 'restore names', 'decrypt strings', 'code is unreadable', 'variable names are garbled', 'remove ConfuserEx', or 'remove Dotfuscator'. Use dotnet-analyze if only obfuscation detection is needed."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET Assembly Deobfuscation

Uses dnlib to clean obfuscated .NET assemblies and produce analyzable, clean binaries.

## Prerequisites

- .NET 8 SDK
- Shared project: Run `scripts/setup-project.sh` from the `dotnet-analyze` skill

## 4-Stage Deobfuscation Pipeline

### Stage 1: Name Restoration

Replaces obfuscated names with meaningful names inferred from type and usage context.

**Name restoration strategy:**

| Target | Restoration Rule | Example |
|--------|-----------------|---------|
| Type (Class) | `{Kind}_{Namespace}_{Seq}` | `Class_Services_001` |
| Type (Interface) | `IFace_{Namespace}_{Seq}` | `IFace_Data_002` |
| Type (Enum) | `Enum_{Namespace}_{Seq}` | `Enum_Models_003` |
| Method (void return) | `Do_{Seq}` or `Process_{Seq}` | `Do_0012` |
| Method (bool return) | `Check_{Seq}` | `Check_0015` |
| Method (string return) | `GetText_{Seq}` | `GetText_0018` |
| Method (collection return) | `GetList_{Seq}` | `GetList_0020` |
| Field (static) | `s_field_{Seq}` | `s_field_0025` |
| Field (bool) | `m_flag_{Seq}` | `m_flag_0030` |
| Field (string) | `m_text_{Seq}` | `m_text_0031` |
| Field (int) | `m_num_{Seq}` | `m_num_0032` |
| Property | `Prop_{Seq}` | `Prop_0040` |

### Stage 2: String Decryption

Handles patterns detectable through static analysis.

**Supported patterns:**
- `ldstr` + `call FromBase64String` → Inline replacement after Base64 decoding
- `ldstr` + `call XorDecrypt` (simple constant key) → XOR decryption attempt
- String proxy method detection (array access with constant index)

**Limitations:**
- Decryption with dynamic keys is not possible through static analysis
- ConfuserEx constant protection requires runtime analysis (de4dot recommended)
- Custom encryption algorithms require manual analysis

### Stage 3: Obfuscation Attribute Removal

Removes CustomAttributes containing the following keywords at module, assembly, and type levels:

`Dotfuscator`, `Obfusc`, `ConfusedBy`, `SmartAssembly`, `Suppress`, `NETGuard`, `Babel`, `Eazfuscator`, `CryptoObfuscator`, `ILProtector`

### Stage 4: Dead Code Cleanup

- Remove consecutive NOP instructions (excluding NOPs that are branch targets)
- Identify unreferenced empty types (reported only, not deleted)

## Script Template

See `references/deobfuscate-template.cs` for the detailed implementation.

## Core Code Pattern

```csharp
using dnlib.DotNet;
using dnlib.DotNet.Writer;

var module = ModuleDefMD.Load(inputPath);

// Name restoration
foreach (var type in module.GetTypes())
{
    if (IsObfuscatedName(type.Name))
        type.Name = $"Class_{counter++:D3}";

    foreach (var method in type.Methods)
    {
        if (method.IsConstructor) continue;
        if (IsObfuscatedName(method.Name))
            method.Name = $"Method_{counter++:D4}";
    }
}

// Save
var options = new ModuleWriterOptions(module)
{
    Logger = DummyLogger.NoThrowInstance  // Ignore errors instead of throwing exceptions
};
module.Write(outputPath, options);
```

## Output

```
┌──────────────────────────────────────┐
│      Deobfuscation Results           │
├─────────────────┬────────────────────┤
│ Names Restored  │ 247                │
│ Strings Decrypted│ 12                │
│ Attributes Removed│ 3               │
│ Dead Code Cleaned│ 1,204            │
│ Total           │ 1,466              │
└─────────────────┴────────────────────┘
✓ Output file: MyApp_cleaned.dll
```

## Recommended Workflow

```
1. Detect obfuscation with dotnet-analyze
     ↓ (obfuscation confirmed)
2. Clean with dotnet-deobfuscate
     ↓ (clean DLL generated)
3. Recover source with dotnet-decompile
     ↓ (readable C# code)
4. Visualize structure with dotnet-callgraph
```

## Advanced: de4dot Integration

For advanced obfuscation such as ConfuserEx, the open-source tool de4dot is recommended:

```bash
# Using de4dot (requires separate installation)
de4dot target.dll -o target_cleaned.dll

# Name restoration from this skill can be additionally applied afterward
```

## Notes

- Deobfuscated DLLs may not execute identically to the original (signature invalidation)
- Assemblies with Strong Names will require re-signing
- Deobfuscating license-protection obfuscation may raise legal concerns
- This skill is intended only for security analysis, compatibility maintenance, and legacy code understanding
