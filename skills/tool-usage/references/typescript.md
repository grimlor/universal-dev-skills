# TypeScript Tool Usage Reference

TypeScript-specific details for applying `tool-usage`.

## Recommended VS Code Extensions

| Extension | ID | Purpose |
|---|---|---|
| TypeScript and JavaScript | `ms-vscode.vscode-typescript-next` | Nightly TS language service (latest inference, go-to-definition) |
| ESLint | `dbaeumer.vscode-eslint` | Inline lint diagnostics from project config |
| Jest | `Orta.vscode-jest` | Inline test status, watch mode, debug integration, coverage gutters |
| Pretty TypeScript Errors | `yoavbls.pretty-ts-errors` | Human-readable formatting of complex TS errors |

The built-in TypeScript language service runs automatically and provides type
checking, IntelliSense, and refactoring support. The nightly extension is
optional but recommended — it picks up TypeScript improvements before stable
releases.

### Jest extension notes

The Jest extension surfaces test results inline and in the status bar
("Jest" for the runner, "Jest-WS" for workspace-level pass/fail counts).

In a **multi-root workspace** where not every folder has Jest, the extension
may show a warning icon (⚠) for folders without a `jest.config.*`. This is
expected — the extension only activates for folders that have a valid Jest
configuration. For a cleaner experience when doing focused TypeScript work,
open the specific project folder rather than the parent workspace.

The `runTests` tool integrates with the Jest extension's test discovery.
Always use `runTests` rather than `jest` in the terminal — the tool handles
path resolution, output formatting, and workspace context that raw CLI
invocation misses.

## Recommended Settings

```jsonc
{
  // Enable strict checking in the editor (matches tsconfig.json strict: true)
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,

  // Auto-organize imports on save
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },

  // ESLint flat config support
  "eslint.useFlatConfig": true,

  // Format on save using ESLint (no separate formatter needed)
  "editor.formatOnSave": true,
  "[typescript]": {
    "editor.defaultFormatter": "dbaeumer.vscode-eslint"
  }
}
```

**Why `typescript.tsdk`:** Points VS Code at the project's own TypeScript
version rather than the globally bundled one. This ensures the editor's
type-checking matches `tsc --noEmit` output exactly — no version drift
between editor and CLI.

## ESLint vs. Problems Panel

ESLint diagnostics appear in the Problems panel alongside TypeScript errors.
Both sources show inline squiggles. Key differences:

- **TypeScript errors** (TS####) come from the language service and match
  `tsc --noEmit` output.
- **ESLint warnings/errors** come from the ESLint extension and match
  `eslint .` output.

After completing edits, run both CLI checks in the terminal as final
verification — the Problems panel may not surface every diagnostic
immediately.

```bash
npm run lint
npm run typecheck
```

## Known ESLint Flat Config Quirk

When switching from legacy `.eslintrc.*` to flat config (`eslint.config.mjs`),
the ESLint extension may continue reading the old config until reloaded. After
creating `eslint.config.mjs` and deleting legacy config files, run
**ESLint: Restart ESLint Server** from the command palette.

## TypeScript Snippet Execution

For quick TypeScript snippets, there is no `RunCodeSnippet` equivalent to
Pylance's Python snippet runner. Use `run_in_terminal` with `npx tsx` for
ad-hoc TypeScript execution when available:

```bash
npx tsx -e "console.log('hello')"
```

For scripts longer than 10 lines, follow the standard script-file fallback
from the core `tool-usage` skill: write to `.copilot/scripts/`, then execute.
