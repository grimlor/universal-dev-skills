# C# Tool Usage Reference

C#-specific details for applying `tool-usage`.

## Recommended VS Code Extensions

| Extension | ID | Purpose |
|---|---|---|
| C# Dev Kit | `ms-dotnettools.csdevkit` | Project system, solution explorer, test discovery |
| C# | `ms-dotnettools.csharp` | Language support (OmniSharp / Roslyn), IntelliSense, debugging |
| .NET Install Tool | `ms-dotnettools.vscode-dotnet-runtime` | Manages .NET SDK installations |

The C# Dev Kit provides solution-level project management, test explorer
integration, and NuGet package management. The base C# extension provides
IntelliSense, go-to-definition, inline diagnostics, refactoring, and
debugging — equivalent to what Pylance does for Python.

### Test runner integration

C# Dev Kit discovers xUnit, NUnit, and MSTest tests and displays them in
the Testing sidebar. Use the `runTests` tool when available; otherwise use
`dotnet test` in the terminal.

## Recommended Settings

```jsonc
{
  // Enable Roslyn analyzers in the editor
  "dotnet.server.useOmnisharp": false,

  // Format on save
  "editor.formatOnSave": true,
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp"
  },

  // Organize usings on save
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },

  // Enable inlay hints for parameter names and types
  "csharp.inlayHints.parameters.enabled": true,
  "csharp.inlayHints.types.enabled": true
}
```

**Why `useOmnisharp: false`:** Uses the newer Roslyn-based language server
(bundled with C# Dev Kit) instead of OmniSharp. This provides better
analyzer support and faster IntelliSense.

## Diagnostics vs. Build Output

C# diagnostics appear in the Problems panel from two sources:

- **Roslyn language server** — real-time compiler errors, warnings, and
  analyzer findings as you type.
- **Build output** — diagnostics from `dotnet build`, including analyzers
  enabled in `.editorconfig` or `Directory.Build.props`.

After completing edits, run the full quality gate in the terminal as final
verification:

```bash
dotnet format --verify-no-changes
dotnet build --warnaserrors
dotnet test
```

## C# Snippet Execution

For quick C# snippets, use `dotnet-script` (install once as a global tool):

```bash
# Install (one time)
dotnet tool install -g dotnet-script

# Run inline
dotnet script eval "Console.WriteLine(\"hello\");"

# Run a .csx script file
dotnet script .copilot/scripts/snippet.csx
```

For scripts that need project dependencies, prefer writing a small test or
a console app entry point and running via `dotnet run`.

For scripts longer than 10 lines, follow the standard script-file fallback
from the core `tool-usage` skill: write to `.copilot/scripts/`, then execute.

## dotnet CLI Conventions

Always use the `dotnet` CLI rather than MSBuild directly:

```bash
# ✅ Standard CLI
dotnet build
dotnet test
dotnet format

# ❌ Direct MSBuild — less portable
msbuild /t:Build
```

The `dotnet` CLI wraps MSBuild and provides consistent cross-platform
behavior.
