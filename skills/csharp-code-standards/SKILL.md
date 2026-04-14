---
name: csharp-code-standards
description: "Roslyn analyzer, .editorconfig, and build configuration standards for C# / .NET projects. Use when setting up a new .NET project, auditing an existing project's tooling config, or applying lint/type-checking fixes. Covers the dotnet CLI, xUnit, FluentAssertions, and pre-commit hooks."
---

# C# Code Standards

> **Forward-looking skill.** This skill was authored before any live C# projects
> exist in the workspace. Refine canonical configs and common fix patterns when
> real project usage begins.

## When This Skill Applies

Whenever:
- Setting up tooling in a new C#/.NET project
- Auditing or updating `.csproj`, `Directory.Build.props`, or `.editorconfig`
- Running Roslyn analyzers, `dotnet format`, or the compiler to find and fix issues
- Adding or updating pre-commit hooks or CI quality gates
- Applying the standard build/test/lint tasks

---

## Scope -- Personal vs. Team Projects

**This standard applies in full only to projects where you control the toolchain**
(personal projects, greenfield repos, repos where you are the sole or primary
author).

### How to determine if you control the toolchain

1. **GitHub owner is `grimlor`** → personal repo → full standard applies.
2. **Forked repo** (different owner, contributor commits from `grimlor`) → apply
   the higher bar of your personal standard and the upstream's standard to your
   contributions. Don't rewrite the upstream's existing configs -- the upstream
   project's conventions (analyzer rules, test framework, project structure) are
   theirs to own.
3. **Repo lives under a work org path or an ADO workspace** → team repo → follow
   team conventions for shared config, but apply the higher bar of your personal
   standard and the team's standard to your own contributions. You may not be
   able to reduce existing tech debt, but don't add to it.
4. **`.csproj` or `Directory.Build.props` already has a different analyzer setup**
   → someone else owns the config; don't replace it without team agreement.
5. **`CODEOWNERS` file exists or git log shows multiple authors** → shared
   codebase; don't commit toolchain changes unilaterally.

When in doubt, ask the user which category the repo falls into before applying the
full standard.

**Important:** Do not treat configs from forked projects as canonical examples of
this standard. Forked project configs reflect the original author's choices, not
necessarily yours.

At work or in open-source contributions, team repos may follow different
conventions -- and that's expected. Key differences to watch for:

- **Target framework:** teams may target different .NET versions. Match theirs.
- **Test framework:** teams may use NUnit or MSTest instead of xUnit. Don't
  migrate test frameworks without team agreement.
- **Analyzers:** teams may use SonarAnalyzer, StyleCop, or a custom ruleset.
  Adapt to what's configured.
- **Project structure:** some teams use `Directory.Build.props` for shared config,
  others inline everything in `.csproj`. Follow the established pattern.

In team contexts, apply what you can personally (enabling nullable reference types
in your files, running analyzers locally) without imposing changes on shared config
files. Your contributed code should still meet your personal quality bar even when
the team's bar is lower.

---

## Target Framework

**Target .NET 8 (LTS) for personal projects.** Adjust to the team's minimum when
contributing to shared codebases.

```xml
<!-- .csproj -->
<PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
</PropertyGroup>
```

---

## Canonical `Directory.Build.props`

Place at the solution root. These properties apply to all projects in the solution:

```xml
<Project>
    <PropertyGroup>
        <!-- Language version -->
        <LangVersion>latest</LangVersion>
        <Nullable>enable</Nullable>
        <ImplicitUsings>enable</ImplicitUsings>

        <!-- Treat all warnings as errors -->
        <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
        <WarningsAsErrors />
        <NoWarn />

        <!-- Analysis -->
        <AnalysisLevel>latest-all</AnalysisLevel>
        <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
        <EnableNETAnalyzers>true</EnableNETAnalyzers>
    </PropertyGroup>
</Project>
```

**Why `TreatWarningsAsErrors`:** Same principle as Java's `-Werror` and
TypeScript's `strict: true` -- catch problems at compile time, not in production.

**Why `AnalysisLevel=latest-all`:** Enables common Roslyn style, design, and
security analyzers at their strictest level. This is the C# equivalent of
enabling all Checkstyle + SpotBugs rules.

**Why `Nullable=enable`:** Nullable reference types are C#'s most impactful
type-safety feature -- the equivalent of TypeScript's `strictNullChecks`. Enabling
it catches null-related bugs at compile time.

---

## Canonical `.editorconfig`

Place at the solution root. Controls code style enforcement during build:

```ini
# Top-most EditorConfig file
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
# Namespace declarations
csharp_style_namespace_declarations = file_scoped:warning

# var preferences
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:suggestion

# Expression-bodied members
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_constructors = false:suggestion
csharp_style_expression_bodied_properties = true:suggestion
csharp_style_expression_bodied_accessors = true:suggestion

# Pattern matching
csharp_style_pattern_matching_over_is_with_cast_check = true:warning
csharp_style_pattern_matching_over_as_with_null_check = true:warning

# Null checking
csharp_style_throw_expression = true:suggestion
csharp_style_conditional_delegate_call = true:suggestion

# Using directives
csharp_using_directive_placement = outside_namespace:warning
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = true

# Naming conventions
dotnet_naming_rule.public_members_must_be_pascal_case.severity = warning
dotnet_naming_rule.public_members_must_be_pascal_case.symbols = public_symbols
dotnet_naming_rule.public_members_must_be_pascal_case.style = pascal_case_style

dotnet_naming_symbols.public_symbols.applicable_kinds = class,struct,interface,enum,property,method,event,delegate
dotnet_naming_symbols.public_symbols.applicable_accessibilities = public,internal,protected

dotnet_naming_style.pascal_case_style.capitalization = pascal_case

dotnet_naming_rule.private_fields_must_be_camel_case.severity = warning
dotnet_naming_rule.private_fields_must_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_must_be_camel_case.style = camel_case_underscore_style

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.camel_case_underscore_style.required_prefix = _
dotnet_naming_style.camel_case_underscore_style.capitalization = camel_case

# XML documentation
dotnet_diagnostic.CS1591.severity = warning

[*.{csproj,props,targets}]
indent_size = 2
```

---

## XML Documentation Standard

All public symbols must have XML documentation comments -- classes, interfaces,
methods, properties, and constructors. The `CS1591` warning (enforced via
`.editorconfig`) catches missing documentation.

Enable documentation generation in each project:

```xml
<!-- .csproj -->
<PropertyGroup>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

### XML doc format

```csharp
/// <summary>
/// Parse a duration string into milliseconds.
/// </summary>
/// <param name="input">Human-readable duration like "5m" or "2h30m".</param>
/// <returns>The duration in milliseconds.</returns>
/// <exception cref="FormatException">
/// Thrown when <paramref name="input"/> format is unrecognized.
/// </exception>
public long ParseDuration(string input)
{
    // ...
}
```

### Common XML doc patterns

**Class:**
```csharp
/// <summary>
/// Manages retry logic with exponential backoff.
/// </summary>
/// <remarks>
/// Thread-safe. Each instance maintains its own retry counter.
/// </remarks>
public class RetryPolicy
{
    /// <summary>
    /// Initializes a new instance of <see cref="RetryPolicy"/>.
    /// </summary>
    /// <param name="maxRetries">Maximum number of retry attempts.</param>
    /// <param name="baseDelay">Base delay between retries.</param>
    public RetryPolicy(int maxRetries, TimeSpan baseDelay)
    {
        // ...
    }
}
```

**Interface:**
```csharp
/// <summary>
/// Storage adapter for persisting application state.
/// </summary>
/// <remarks>
/// Implementations must be safe for concurrent access.
/// </remarks>
public interface IStorageAdapter
{
    /// <summary>
    /// Store a value by key, overwriting any previous value.
    /// </summary>
    /// <param name="key">The storage key.</param>
    /// <param name="value">The value to store.</param>
    void Put(string key, string value);
}
```

**Tests do not require XML documentation** -- the test method names and
`[Fact]`/`[Theory]` attributes serve as the specification.

---

## Test Framework Configuration

**Use xUnit for all personal projects.** Add FluentAssertions for expressive
assertions and Moq for mocking.

### Test project `.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
    <PropertyGroup>
        <TargetFramework>net8.0</TargetFramework>
        <Nullable>enable</Nullable>
        <IsPackable>false</IsPackable>
        <IsTestProject>true</IsTestProject>
    </PropertyGroup>

    <ItemGroup>
        <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
        <PackageReference Include="xunit" Version="2.*" />
        <PackageReference Include="xunit.runner.visualstudio" Version="2.*" />
        <PackageReference Include="FluentAssertions" Version="7.*" />
        <PackageReference Include="Moq" Version="4.*" />
        <PackageReference Include="coverlet.collector" Version="6.*" />
    </ItemGroup>

    <ItemGroup>
        <ProjectReference Include="..\YourProject\YourProject.csproj" />
    </ItemGroup>
</Project>
```

### Coverage threshold

```bash
dotnet test --collect:"XPlat Code Coverage" \
    /p:CollectCoverage=true \
    /p:Threshold=100 \
    /p:ThresholdType=line \
    /p:ThresholdStat=total
```

**Coverage threshold:** 100% line coverage for personal projects. For contributed
or forked projects, match the upstream's threshold.

---

## Standard CLI Commands

| Command | Purpose |
|---|---|
| `dotnet build --warnaserrors` | Compile with warnings as errors |
| `dotnet test` | Run all tests |
| `dotnet test --collect:"XPlat Code Coverage"` | Run tests with coverage |
| `dotnet format --verify-no-changes` | Verify formatting without modifying |
| `dotnet format` | Auto-format source code |
| `dotnet format analyzers` | Run and fix analyzer warnings |
| `dotnet build /p:TreatWarningsAsErrors=true` | Strict build (if not in props) |

### Composite quality gate

Create a script or `Makefile` target that runs the full gate:

```bash
#!/bin/bash
# scripts/check.sh -- full quality gate
set -euo pipefail

dotnet format --verify-no-changes
dotnet build --warnaserrors
dotnet test --collect:"XPlat Code Coverage" \
    /p:CollectCoverage=true \
    /p:Threshold=100 \
    /p:ThresholdType=line \
    /p:ThresholdStat=total
```

This is the C# equivalent of `./gradlew check` (Java), `npm run check`
(TypeScript), or `task check` (Python).

---

## Pre-commit Hooks

For personal C# projects, use a pre-commit hook that runs formatting and
compilation checks.

### Using pre-commit framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: dotnet-format
        name: dotnet-format
        entry: dotnet format --verify-no-changes
        language: system
        pass_filenames: false
        types: [c#]
      - id: dotnet-build
        name: dotnet-build
        entry: dotnet build --no-restore --warnaserrors
        language: system
        pass_filenames: false
        types: [c#]
```

### Using Husky.Net

```bash
dotnet tool install Husky
dotnet husky install
dotnet husky add pre-commit -c "dotnet format --verify-no-changes && dotnet build --no-restore --warnaserrors"
```

Running the full quality gate (including tests) in a pre-commit hook is viable
for small projects but may be too slow for large solutions. At minimum, format
and compile -- reserve the full gate for CI or a manual pre-push check.

---

## Suppression Policy

### `#pragma warning disable`

- Always specify the exact diagnostic ID being suppressed.
- Always include a comment explaining why.
- Use the narrowest scope possible (`#pragma warning disable` / `#pragma warning
  restore` around the specific line).
- File-level or project-level suppression is never acceptable in source code.

```csharp
// ❌ Broad suppression
#pragma warning disable

// ❌ No reason
#pragma warning disable CS8618

// ✅ Specific with reason and restore
#pragma warning disable CS8618 // Non-nullable field -- initialized by DI framework
private readonly ILogger _logger;
#pragma warning restore CS8618
```

### `[SuppressMessage]`

Same rules -- narrow scope, specific diagnostic, always include a justification:

```csharp
[SuppressMessage(
    "Design",
    "CA1062:Validate arguments of public methods",
    Justification = "Parameter validated by FluentValidation middleware")]
public void Process(Request request)
{
    // ...
}
```

---

## Common Nullable Reference Type Fix Patterns

When enabling `<Nullable>enable</Nullable>`, these patterns address the most
common warnings without reaching for `#pragma warning disable`.

### Null-forgiving operator (use sparingly)

```csharp
// ❌ Silences all null warnings on this expression
var name = user!.Name!;

// ✅ Guard clause -- compiler flow analysis eliminates the warning
if (user is null) throw new ArgumentNullException(nameof(user));
var name = user.Name;

// ✅ Null-forgiving is acceptable for test setup or DI patterns where you
// know the value will be set before use
private ILogger _logger = null!; // Set by DI container
```

### Nullable return types

```csharp
// ❌ Warning: possible null reference return
public string FindName(int id)
{
    return _map.GetValueOrDefault(id); // may be null
}

// ✅ Explicit nullable return signals absence
public string? FindName(int id)
{
    return _map.GetValueOrDefault(id);
}
```

### Null-coalescing and null-conditional

```csharp
// ❌ Warning: possible null dereference
var length = user.Name.Length;

// ✅ Null-safe access
var length = user?.Name?.Length ?? 0;

// ✅ Throw if null (for non-nullable expectations)
var length = (user?.Name ?? throw new InvalidOperationException("Name required")).Length;
```

### Pattern matching for null checks

```csharp
// ❌ Classic null check
if (result != null)
{
    Process(result);
}

// ✅ Pattern matching -- cleaner and compiler-aware
if (result is { } validResult)
{
    Process(validResult);
}

// ✅ Switch expression with patterns
var message = status switch
{
    Status.Active => "Running",
    Status.Inactive => "Stopped",
    null => "Unknown",
    _ => throw new ArgumentOutOfRangeException(nameof(status))
};
```

### Required members (C# 11+)

```csharp
// ❌ Mutable properties with nullable warnings
public class Config
{
    public string ApiUrl { get; set; } // CS8618
    public int Timeout { get; set; }
}

// ✅ Required members -- compiler enforces initialization
public class Config
{
    public required string ApiUrl { get; init; }
    public required int Timeout { get; init; }
}
```

### Records for immutable data

```csharp
// ❌ Boilerplate class with equality
public class Config
{
    public string ApiUrl { get; }
    public int Timeout { get; }
    // constructor, equality, hashCode, toString...
}

// ✅ Record -- immutable by default, no boilerplate
public record Config(string ApiUrl, int Timeout);
```

---

## Dev Dependencies

Standard NuGet packages for a new C#/.NET project:

**Test project:**
- `Microsoft.NET.Test.Sdk` -- test runner infrastructure
- `xunit` -- test framework
- `xunit.runner.visualstudio` -- VS Code/VS test discovery
- `FluentAssertions` -- fluent assertion library
- `Moq` -- mocking framework
- `coverlet.collector` -- code coverage collection

**Analyzers (referenced from main project or `Directory.Build.props`):**

```xml
<ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="8.*">
        <PrivateAssets>all</PrivateAssets>
        <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
</ItemGroup>
```

The `Microsoft.CodeAnalysis.NetAnalyzers` package is included by default with
`EnableNETAnalyzers=true`, but you can pin a specific version via a package
reference for consistent behavior across machines.

---

## Workflow for Applying Standards to an Existing Project

**For personal projects:** apply the full standard below.
**For team projects:** see [Scope](#scope--personal-vs-team-projects) first -- only
apply what the team has agreed to, or what doesn't affect shared config.

1. **Create `Directory.Build.props`** at the solution root with the canonical
   properties (nullable, warnings as errors, analysis level).

2. **Create `.editorconfig`** at the solution root with the canonical style rules.

3. **Enable documentation generation** -- add `<GenerateDocumentationFile>` to
   each project's `.csproj`.

4. **Set up test project** -- configure xUnit, FluentAssertions, Moq, and Coverlet
   per the canonical test project config.

5. **Run formatter:** `dotnet format`

6. **Run build with analysis:** `dotnet build --warnaserrors`

7. **Fix nullable warnings** -- apply the fix patterns above. Start at leaf types
   (models, DTOs) and work upward to services and controllers.

8. **Fix remaining analyzer warnings** -- `dotnet format analyzers` can auto-fix
   some; the rest require manual fixes guided by the diagnostic IDs.

9. **Verify clean:** `scripts/check.sh` should pass with no warnings.

10. **Set up pre-commit hooks** -- configure pre-commit or Husky.Net.

11. **Commit:** `chore(build): add Roslyn analyzers, nullable references, and strict warnings`
