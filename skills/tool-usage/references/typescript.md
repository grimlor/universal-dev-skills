# TypeScript Tool Usage Reference

TypeScript-specific details for applying `tool-usage`.

## Recommended VS Code Extensions

| Extension | ID | Purpose |
|---|---|---|
| TypeScript and JavaScript | `ms-vscode.vscode-typescript-next` | Nightly TS language service (latest inference, go-to-definition) |
| ESLint | `dbaeumer.vscode-eslint` | Inline lint diagnostics from project config |
| Jest | `Orta.vscode-jest` | Inline test status, watch mode, debug integration, coverage gutters |
| Pretty TypeScript Errors | `yoavbls.pretty-ts-errors` | Human-readable formatting of complex TS errors |
| Bun | `oven.bun-vscode` | Bun runtime integration -- debugging, `bun.lock` support, Bun-based test discovery |

The built-in TypeScript language service runs automatically and provides type
checking, IntelliSense, and refactoring support. The nightly extension is
optional but recommended -- it picks up TypeScript improvements before stable
releases.

### Jest extension notes

The Jest extension surfaces test results inline and in the status bar
("Jest" for the runner, "Jest-WS" for workspace-level pass/fail counts).

In a **multi-root workspace** where not every folder has Jest, the extension
may show a warning icon (⚠) for folders without a `jest.config.*`. This is
expected -- the extension only activates for folders that have a valid Jest
configuration. For a cleaner experience when doing focused TypeScript work,
open the specific project folder rather than the parent workspace.

The `runTests` tool integrates with the Jest extension's test discovery.
Always use `runTests` rather than `jest` in the terminal -- the tool handles
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
type-checking matches `tsc --noEmit` output exactly -- no version drift
between editor and CLI.

## ESLint vs. Problems Panel

ESLint diagnostics appear in the Problems panel alongside TypeScript errors.
Both sources show inline squiggles. Key differences:

- **TypeScript errors** (TS####) come from the language service and match
  `tsc --noEmit` output.
- **ESLint warnings/errors** come from the ESLint extension and match
  `eslint .` output.

After completing edits, run both CLI checks in the terminal as final
verification -- the Problems panel may not surface every diagnostic
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

There is no language-server snippet tool for TypeScript (unlike Python's
Pylance `RunCodeSnippet`). Direct interpreter invocations (`npx tsx`,
`bun -e`, `bun <file.ts>`) are blocked by the hook -- they bypass user review.

For ad-hoc TypeScript execution, follow the Script Handling rules from the
core `tool-usage` skill:

1. Write the script to `.copilot/scripts/<name>.ts`.
2. Show it to the user in a code block.
3. Ask the user to approve running it.

## Bun Runtime Notes

Bun is an alternative JavaScript/TypeScript runtime that can replace Node.js,
npm, and Jest in projects that adopt it. The Bun VS Code extension
(`oven.bun-vscode`) provides debugging support and `bun.lock` file handling.

**When to use Bun CLI commands:**

| Task | Command | Notes |
|------|---------|-------|
| Install dependencies | `bun install` | Equivalent to `npm install` |
| Add a package | `bun add <pkg>` | Equivalent to `npm install <pkg>` |

**Bun's built-in test runner** (`bun test`) is subject to the same rule as
Jest, Vitest, and Mocha: use the `runTests` tool rather than running tests in
the terminal.

**Bun coverage via `runTests`:** The `runTests` tool's response payload
contains only a pass/fail summary -- no coverage table, no file-level
breakdown. However, when `bunfig.toml` has `coverage = true` and
`coverageReporter = ["text", "lcov"]`, `runTests` **does** trigger Bun's
coverage engine under the hood. The lcov file is written to
`coverage/lcov.info` (relative to the repo root) on every run.

**Agent workflow for Bun coverage:**

1. Use `runTests` to execute tests (standard rule -- no terminal needed).
2. Read `coverage/lcov.info` via `read_file` to get file-level coverage data.
3. The lcov file is regenerated on each `runTests` invocation, so it always
   reflects the most recent run.

This requires `bunfig.toml` with the lcov reporter configured. If
`bunfig.toml` does not exist (e.g. contributed projects), create one locally
with coverage settings -- it does not need to be committed.

Detect a Bun-based project by the presence of `bun.lock` or `bun.lockb` in the
project root. When present, prefer `bun` over `npm` for package management.
`bun run`, `npx`, and `bunx` are all blocked -- they can execute arbitrary code.
