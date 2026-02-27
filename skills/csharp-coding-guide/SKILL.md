---
name: csharp-coding-guide
description: "C# and .NET coding reference guide with mandatory research workflow. Use when writing C# code, planning C# architecture, refactoring C# code, analyzing C# errors, reviewing C# code, or working with any .NET framework (ASP.NET, Blazor, MAUI, WPF, WinForms, Entity Framework, etc.). Triggers on: C# code writing, C# error analysis, C# refactoring, .NET project planning, .NET API usage questions, NuGet package selection, or any C#/.NET development task. Enforces a 3-step reference order: (1) Microsoft official docs, (2) StackOverflow, (3) GitHub."
---

# C# / .NET Coding Reference Guide

Enforce the following research-first workflow for all C#/.NET development tasks. Always search external sources before writing or modifying code.

## Mandatory Reference Order

Execute these steps **in order**. Each step uses `WebSearch` and/or `WebFetch`.

### Step 1: Microsoft Official Documentation

Search Microsoft Learn (learn.microsoft.com) first. This is the authoritative source.

**Search patterns:**
```
WebSearch: "site:learn.microsoft.com {keyword} C#"
WebSearch: "site:learn.microsoft.com {class/method name} .NET"
WebSearch: "site:learn.microsoft.com {framework} tutorial"
```

**What to look for:**
- Official API reference and method signatures
- Recommended patterns and best practices
- Sample code from Microsoft
- Breaking changes and migration guides (when upgrading)
- Performance guidance and known limitations

**When to use WebFetch:**
- Load the specific API doc page to get exact method signatures and parameters
- Load sample code pages for implementation patterns

### Step 2: StackOverflow

Search StackOverflow for real-world solutions and edge cases.

**Search patterns:**
```
WebSearch: "site:stackoverflow.com {error message} C#"
WebSearch: "site:stackoverflow.com {task description} .NET"
WebSearch: "site:stackoverflow.com {class name} {specific problem}"
```

**What to look for:**
- Accepted answers with high vote counts
- Common pitfalls and workarounds
- Edge cases not covered in official docs
- Performance comparisons between approaches
- Version-specific solutions (check answer dates and .NET version)

**Caution:**
- Prefer answers targeting .NET 6+ over legacy .NET Framework answers
- Verify outdated answers against current API (older answers may use deprecated APIs)

### Step 3: GitHub

Search GitHub for real project implementations and patterns.

**Search patterns:**
```
WebSearch: "site:github.com {pattern/library} C# example"
WebSearch: "site:github.com {NuGet package name} usage"
WebSearch: "{task description} C# github repository"
```

**What to look for:**
- Open-source project implementations as reference
- NuGet package usage examples
- Project structure patterns
- Test code for usage examples
- README and documentation for libraries

## Task-Specific Workflow

### Code Writing / New Feature

1. **MS Docs**: Search API reference for classes/methods to use
2. **SO**: Search for common implementation patterns and pitfalls
3. **GitHub**: Find similar open-source implementations for reference
4. Write code incorporating findings

### Error Analysis / Debugging

1. **MS Docs**: Search the error code or exception type for official explanation
2. **SO**: Search the exact error message for community solutions
3. **GitHub**: Search Issues for the same error in related projects
4. Propose fix based on findings

### Refactoring

1. **MS Docs**: Check current best practices and recommended patterns
2. **SO**: Search for performance/maintainability discussions on the pattern
3. **GitHub**: Find examples of the target pattern in production code
4. Refactor with evidence-based approach

### Architecture / Planning

1. **MS Docs**: Review architecture guides and reference architectures
2. **SO**: Search for trade-off discussions and scaling experiences
3. **GitHub**: Examine project structures in popular .NET repositories
4. Present options with references

### NuGet Package Selection

1. **MS Docs**: Check if a built-in solution exists first
2. **SO**: Compare recommendations and reported issues
3. **GitHub**: Check repo stars, maintenance activity, and open issues
4. Recommend with rationale

## Output Format

After research, summarize findings before writing code:

```
## Research Summary
- **MS Docs**: [key finding or link]
- **StackOverflow**: [relevant answer or "no relevant results"]
- **GitHub**: [reference project or "no relevant results"]
- **Decision**: [chosen approach and why]
```

## When to Skip Steps

- **Trivial syntax**: Skip research for basic language constructs (if/else, loops, string interpolation)
- **Already-known API**: Skip if the exact API usage is confidently known and well-established
- **Step returned no results**: Note "no relevant results" and proceed to next step
- **User explicitly says "skip research"**: Respect the user's request

## Notes

- Always cite sources when referencing external findings
- Prefer latest .NET LTS version patterns unless the project targets a specific version
- When multiple valid approaches exist, present options with trade-offs from research
- Korean language preferred for explanations and summaries
