---
name: typescript-code-standards
description: "ESLint, TypeScript compiler, and Jest configuration standards for TypeScript projects. Use when setting up a new TypeScript project, auditing an existing project's tooling config, or applying lint/type-checking fixes. Covers tsconfig.json, ESLint flat config, Jest setup, and Husky pre-commit hooks."
---

# TypeScript Code Standards

## When This Skill Applies

Whenever:
- Setting up tooling in a new TypeScript project
- Auditing or updating `tsconfig.json`, ESLint, or Jest configuration
- Running `tsc --noEmit` or ESLint to find and fix issues
- Adding or updating pre-commit hooks (Husky + lint-staged)
- Applying the standard npm scripts

---

## Scope — Personal vs. Team Projects

**This standard applies in full only to projects where you control the toolchain**
(personal projects, greenfield repos, repos where you are the sole or primary
author).

### How to determine if you control the toolchain

1. **GitHub owner is `grimlor`** → personal repo → full standard applies.
2. **Forked repo** (different owner, contributor commits from `grimlor`) → apply
   the higher bar of your personal standard and the upstream's standard to your
   contributions. Don't rewrite the upstream's existing configs — the upstream
   project's conventions (coverage thresholds, lint rules, formatting) are
   theirs to own.
3. **Repo lives under a work org path or an ADO workspace** → team repo → follow
   team conventions for shared config, but apply the higher bar of your personal
   standard and the team's standard to your own contributions. You may not be
   able to reduce existing tech debt, but don't add to it.
4. **`tsconfig.json` already has non-standard settings or a different base** →
   someone else owns the config; don't replace it without team agreement.
5. **`CODEOWNERS` file exists or git log shows multiple authors** → shared
   codebase; don't commit toolchain changes unilaterally.
6. **An `.eslintrc.*` or legacy ESLint config is already present** → adapt to
   what's there rather than overwriting with flat config.

When in doubt, ask the user which category the repo falls into before applying the
full standard.

**Important:** Do not treat configs from forked projects as canonical examples of
this standard. Forked project configs reflect the original author's choices, not
necessarily yours.

At work or in open-source contributions, team repos may follow different
conventions — and that's expected. Key differences to watch for:

- **ESLint format:** team repos may use legacy `.eslintrc.*` instead of flat
  config. Don't rewrite to flat config unilaterally.
- **Formatter:** teams may use Prettier, Biome, or ESLint formatting rules. Match
  what's configured — don't introduce a different formatter.
- **Package manager:** team repos may use pnpm, yarn, or bun. Use whatever
  `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lock` indicates.
- **Test framework:** some teams use Vitest instead of Jest. Adapt to what's there.
- **Build tool:** teams may use webpack, rollup, or tsc directly. Don't replace
  with esbuild unilaterally.

In team contexts, apply what you can personally (running ESLint locally, using strict
TypeScript in your editor) without imposing changes on shared config files. Your
contributed code should still meet your personal quality bar even when the team's
bar is lower.

---

## Package Manager

**Prefer npm for all personal projects.** Use `npm install`, `npm run`, and
`package-lock.json`.

For team/open-source projects, use whatever lock file is present:

| Lock file | Package manager |
|---|---|
| `package-lock.json` | npm |
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `bun.lock` or `bun.lockb` | bun |

When the project uses Bun (detected by `bun.lock` or `bun.lockb`), use `bun`
equivalents for package management commands:

| npm command | Bun equivalent |
|---|---|
| `npm install` | `bun install` |
| `npm install <pkg>` | `bun add <pkg>` |
| `npm install -D <pkg>` | `bun add -d <pkg>` |

`bun run`, `npx`, and `bunx` are all blocked by the hook — they can execute
arbitrary code. Direct file execution (`bun <file.ts>`, `bun dev`) is also
blocked. Write scripts to files and ask the user to approve running them.

---

## Canonical `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "types": ["jest", "node"]
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Why `strict: true`:** Enables all strict type-checking flags as a group
(`noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`,
`strictBindCallApply`, `strictPropertyInitialization`,
`noImplicitThis`, `alwaysStrict`). The additional `noUnused*` and `noImplicit*`
flags above go beyond what `strict` enables.

**Adjust `target` and `lib` to match the runtime:**
- Browser extensions: `ES2020` + `["ES2020", "DOM"]`
- Node.js server: `ES2022` + `["ES2022"]` (no DOM)
- Obsidian plugins: `ES2018` + `["ES2018", "DOM"]` (older runtime)

**Adjust `types` to match the project:**
- Browser extensions: `["chrome", "jest", "node"]`
- Node.js projects: `["jest", "node"]`
- Projects without Jest: omit `"jest"` and add the relevant test framework types

### `tsconfig.test.json`

Jest requires CommonJS modules. Create a separate tsconfig for test compilation:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "module": "commonjs",
    "types": ["jest", "node"]
  },
  "include": ["tests/**/*", "src/**/*"]
}
```

---

## Canonical ESLint Configuration (Flat Config)

All new personal projects must use ESLint v9+ flat config (`eslint.config.mjs`).

```js
import globals from 'globals';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';
import jsdoc from 'eslint-plugin-jsdoc';
import importPlugin from 'eslint-plugin-import';

export default [
  {
    ignores: ['node_modules/**', 'coverage/**', 'dist/**'],
  },
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
      },
      globals: {
        ...globals.browser,
      },
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'jsdoc': jsdoc,
      'import': importPlugin,
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      'indent': ['error', 2],
      'linebreak-style': ['error', 'unix'],
      'quotes': ['error', 'single'],
      'semi': ['error', 'always'],
      'no-console': 'off',
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
      }],
      '@typescript-eslint/no-explicit-any': 'error',
      'jsdoc/require-jsdoc': ['error', {
        publicOnly: true,
        require: { FunctionDeclaration: true, MethodDefinition: true, ClassDeclaration: true },
      }],
      'jsdoc/require-description': 'error',
      'jsdoc/require-param-description': 'error',
      'jsdoc/require-returns-description': 'error',
      'import/order': ['error', {
        'groups': ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        'newlines-between': 'never',
        'alphabetize': { order: 'asc', caseInsensitive: true },
      }],
    },
  },
  {
    files: ['tests/**/*.ts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
      },
      globals: {
        ...globals.jest,
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@typescript-eslint': tseslint,
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      'indent': ['error', 2],
      'linebreak-style': ['error', 'unix'],
      'quotes': ['error', 'single'],
      'semi': ['error', 'always'],
      'no-console': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
  {
    files: ['*.config.js', '*.config.mjs'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.node,
      },
    },
  },
];
```

**Key rules explained:**

| Rule | Setting | Rationale |
|---|---|---|
| `no-explicit-any` | `error` in src, `off` in tests | Source code must be typed; tests may need `any` for mocks and dynamic assertions |
| `no-unused-vars` | `argsIgnorePattern: '^_'` | Prefix unused parameters with `_` instead of suppressing the whole rule |
| `no-console` | `off` | Appropriate for extensions and CLI tools; tighten to `warn` for library code |
| `indent` | 2 spaces | Consistent with the ecosystem norm |
| `quotes` | single | Consistent across all personal projects |
| `semi` | always | Prevents ASI edge cases |
| `jsdoc/require-jsdoc` | `error` (publicOnly) | All exported functions, methods, and classes must have JSDoc |
| `jsdoc/require-description` | `error` | JSDoc must contain a meaningful description, not just tags |
| `import/order` | alphabetized, grouped | Deterministic import ordering prevents merge conflicts and import entropy |

**Adjust globals to match the runtime:**
- Browser extensions: add `chrome: 'readonly'` to src globals
- Node.js projects: use `...globals.node` instead of `...globals.browser`
- Projects with both: merge both globals objects

---

## Canonical Jest Configuration

```js
export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  testMatch: ['**/tests/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!node_modules/**',
    '!tests/**',
    '!dist/**',
  ],
  coverageThreshold: {
    global: {
      branches: 100,
      functions: 100,
      lines: 100,
      statements: 100,
    },
  },
  verbose: true,
  moduleFileExtensions: ['ts', 'js'],
  transform: {
    '^.+\\.ts$': ['ts-jest', {
      tsconfig: 'tsconfig.test.json',
      isolatedModules: true,
    }],
  },
};
```

**Adjust `testEnvironment` to match the project:**
- Browser extensions / DOM manipulation: `jsdom`
- Node.js / server code: `node`

**Coverage threshold:** 100% across all metrics for personal projects. This
aligns with the `bdd-testing` skill's principle that coverage equals complete
specification — every line of production code must have a spec justifying it.
For contributed or forked projects, match the upstream's threshold.

---

## Canonical `bunfig.toml` (Bun Projects)

When using Bun as the test runner instead of Jest, configure coverage and
thresholds in `bunfig.toml` rather than a Jest config file.

```toml
[test]
coverage = true
coverageThreshold = { lines = 1.0, functions = 1.0, statements = 1.0 }
coverageSkipTestFiles = true
coverageReporter = ["text", "lcov"]
```

**Key settings:**

| Setting | Value | Rationale |
|---|---|---|
| `coverage` | `true` | Enables coverage on every `bun test` run, including via `runTests` |
| `coverageThreshold` | `1.0` for all metrics | 100% coverage requirement for personal projects |
| `coverageSkipTestFiles` | `true` | Excludes test files from the coverage report |
| `coverageReporter` | `["text", "lcov"]` | Console output for humans, lcov for CI and editor integration |

**Important: `bunfig.toml` is discovered by walking up parent directories.**
A single config at the repo root covers all packages in a monorepo. With
`coverage = true`, every `bun test` invocation — including via `runTests` —
produces coverage output automatically.

For contributed or team projects, create `bunfig.toml` locally with coverage
settings — it does not need to be committed.

---

## Canonical `package.json` Scripts

```json
{
  "scripts": {
    "build": "esbuild src/<entry>.ts --bundle --format=<format> --outfile=dist/<output>.js --target=es2020",
    "build:watch": "npm run build -- --watch",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "typecheck": "tsc --noEmit",
    "check": "npm run lint && npm run typecheck && npm test",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,js,mjs}": [
      "eslint --fix"
    ]
  }
}
```

The `check` script runs the full quality gate: lint → type-check → test.
Run `npm run check` before pushing to ensure all three pass.

**Substitute `<entry>`, `<format>`, and `<output>`** for the project:
- Browser extension IIFE: `--format=iife --outfile=dist/content.js`
- Node.js ESM: `--format=esm --outfile=dist/index.mjs`
- Library CJS: `--format=cjs --outfile=dist/index.cjs`

**Script naming conventions:**
- `test` — run tests (no coverage)
- `test:coverage` — run tests with coverage report
- `lint` — check only (CI-safe)
- `lint:fix` — check and auto-fix
- `typecheck` — compiler check without emit
- `check` — full quality gate (lint + type-check + test)
- `prepare` — Husky hook installation (runs automatically on `npm install`)

### Bun-based project scripts

When using Bun instead of npm + Jest, define scripts in `package.json`.\nNote that `bun run` is blocked by the hook — the agent cannot invoke these\nscripts directly. Use `runTests` for test execution and rely on pre-commit\nhooks or ask the user to run quality gate scripts manually.

```json
{
  "scripts": {
    "build": "bun build src/<entry>.ts --outfile=dist/<output>.js --target=browser",
    "build:watch": "bun build src/<entry>.ts --outfile=dist/<output>.js --target=browser --watch",
    "test": "bun test",
    "test:watch": "bun test --watch",
    "test:coverage": "bun test --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "typecheck": "tsc --noEmit",
    "check": "eslint . && tsc --noEmit && bun test"
  }
}
```

---

## Pre-commit Hooks (Husky + lint-staged)

Every personal project must have pre-commit hooks that lint staged files.

### Setup

```bash
npm install --save-dev husky lint-staged
npx husky init
```

### `.husky/pre-commit`

```bash
npx lint-staged
tsc --noEmit
```

### lint-staged configuration

Defined in `package.json` (see scripts section above):

```json
{
  "lint-staged": {
    "*.{ts,js,mjs}": [
      "eslint --fix"
    ]
  }
}
```

This runs ESLint with auto-fix on all staged TypeScript and JavaScript files,
then runs `tsc --noEmit` on the full project. While `tsc` cannot check individual
files in isolation, running it in the pre-commit hook ensures type errors don't
slip through. The cost is a full type-check on each commit — acceptable for
the projects in this workspace, which are small enough that `tsc` completes in
seconds.

---

## TypeScript Pragma and Suppression Policy

### `@ts-ignore` / `@ts-expect-error`

- **Prefer `@ts-expect-error` over `@ts-ignore`** — `@ts-expect-error` fails when
  the suppressed error is fixed, preventing stale suppressions.
- Always include a reason comment on the same line.
- File-level `@ts-nocheck` is never acceptable in source code.

```typescript
// ❌ No reason, stale suppression risk
// @ts-ignore
const result = legacyApi.call();

// ✅ Expect-error with reason
// @ts-expect-error -- legacy API missing type stubs, tracked in #42
const result = legacyApi.call();
```

### ESLint disable comments

- Narrow inline disables only — never `eslint-disable` for a whole file.
- Always specify the rule being disabled.
- Always include a reason.

```typescript
// ❌ Broad disable, no reason
/* eslint-disable */

// ❌ No reason
// eslint-disable-next-line @typescript-eslint/no-explicit-any

// ✅ Specific rule with reason
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- third-party SDK returns untyped response
const data: any = sdk.getRawResponse();
```

---

## Dev Dependencies

Standard dev dependencies for a new TypeScript project:

```json
{
  "devDependencies": {
    "@eslint/js": "^9.17",
    "@types/jest": "^29",
    "@types/node": "^22",
    "@typescript-eslint/eslint-plugin": "^8",
    "@typescript-eslint/parser": "^8",
    "esbuild": "^0.24",
    "eslint": "^9",
    "eslint-plugin-import": "^2",
    "eslint-plugin-jsdoc": "^50",
    "globals": "^15",
    "husky": "^9",
    "jest": "^29",
    "lint-staged": "^16",
    "ts-jest": "^29",
    "typescript": "^5"
  }
}
```

Add platform-specific types as needed:
- Browser extensions: `@types/chrome`
- Node.js: `@types/node` (already included above)

---

## JSDoc Documentation Standard

All exported symbols in `src/` must have JSDoc comments — functions, classes,
methods, interfaces, and type aliases. The `eslint-plugin-jsdoc` rules enforce
this. Key requirements:

| Rule enforced | Meaning |
|---|---|
| `jsdoc/require-jsdoc` | All public functions, methods, and classes need JSDoc |
| `jsdoc/require-description` | JSDoc must have a meaningful description body |
| `jsdoc/require-param-description` | `@param` tags must describe the parameter |
| `jsdoc/require-returns-description` | `@returns` tags must describe the return value |

### JSDoc format

```typescript
/**
 * Parse a duration string into milliseconds.
 *
 * @param input - Human-readable duration like "5m" or "2h30m".
 * @returns The duration in milliseconds.
 * @throws {Error} If the input format is unrecognized.
 */
export function parseDuration(input: string): number {
  // ...
}
```

### Common JSDoc patterns

**Interface / type alias:**
```typescript
/** Configuration for the retry policy. */
export interface RetryConfig {
  /** Maximum number of retry attempts. */
  maxRetries: number;
  /** Base delay in milliseconds between retries. */
  baseDelayMs: number;
}
```

**Class:**
```typescript
/**
 * Manages tab lifecycle for the extension popup.
 *
 * Tracks open tabs, handles activation/deactivation, and
 * persists state to chrome.storage.
 */
export class TabManager {
  /**
   * Create a TabManager.
   *
   * @param storage - Chrome storage API adapter.
   */
  constructor(private storage: StorageAdapter) {}
}
```

**Tests do not require JSDoc** — the BDD Given/When/Then `describe`/`it` strings
serve as the specification. JSDoc on test helpers is optional.

---

## Common Strict-Mode Fix Patterns

When enabling `strict: true` on an existing codebase, these patterns address the
most common type errors without reaching for `any` or `@ts-expect-error`.

### Null / undefined narrowing

```typescript
// ❌ Object is possibly 'undefined'
const name = user.profile.name;

// ✅ Guard clause
if (!user.profile) {
  throw new Error('Profile missing');
}
const name = user.profile.name;

// ✅ Optional chaining + nullish coalescing
const name = user.profile?.name ?? 'Anonymous';
```

### Discriminated unions

```typescript
// ❌ Loose union — no way to narrow
type Result = { data: string } | { error: string };

// ✅ Discriminated union — exhaustive narrowing
type Result =
  | { kind: 'success'; data: string }
  | { kind: 'error'; error: string };

function handle(result: Result): string {
  switch (result.kind) {
    case 'success': return result.data;
    case 'error': return result.error;
  }
}
```

### Readonly properties

```typescript
// ❌ Mutable config invites accidental mutation
interface Config {
  apiUrl: string;
  timeout: number;
}

// ✅ Readonly prevents accidental mutation
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// ✅ Or use Readonly<T> for the whole type
function init(config: Readonly<Config>): void { /* ... */ }
```

### Type assertion vs. type guard

```typescript
// ❌ Assertion — bypasses the type checker, no runtime safety
const el = document.getElementById('app') as HTMLDivElement;

// ✅ Type guard — runtime check, compiler knows the narrowing
const el = document.getElementById('app');
if (!(el instanceof HTMLDivElement)) {
  throw new Error('Expected #app to be a div');
}
// el is now HTMLDivElement
```

### Index signatures and `Record`

```typescript
// ❌ Implicit any on bracket access
const value = obj[key];

// ✅ Explicit index signature
const obj: Record<string, number> = {};
const value: number | undefined = obj[key];

// ✅ Or use Map for runtime safety
const map = new Map<string, number>();
const value = map.get(key); // returns number | undefined
```

### Callback types

```typescript
// ❌ Implicit any parameters
const handler = (event) => { /* ... */ };

// ✅ Explicit parameter type
const handler = (event: MouseEvent): void => { /* ... */ };

// ✅ Or let inference work from the context
element.addEventListener('click', (event) => {
  // event is inferred as MouseEvent
});
```

---

## Workflow for Applying Standards to an Existing Project

**For personal projects:** apply the full standard below.
**For team projects:** see [Scope](#scope--personal-vs-team-projects) first — only
apply what the team has agreed to, or what doesn't affect shared config.

1. **Update `tsconfig.json`** — add/replace compiler options per the canonical
   config. Create `tsconfig.test.json` if using Jest with ts-jest.

2. **Set up ESLint** — create `eslint.config.mjs` with the canonical flat config
   (including `eslint-plugin-jsdoc` and `eslint-plugin-import`).
   Remove any legacy `.eslintrc.*` files.

3. **Set up Jest** — create `jest.config.js` with the canonical config. Adjust
   `testEnvironment` for the project type.

4. **Update `package.json` scripts** — add the standard script names
   (`lint`, `lint:fix`, `typecheck`, `check`, `test`, `test:coverage`, `build`).

5. **Set up Husky + lint-staged** — run `npx husky init`, configure `.husky/pre-commit`
   (lint-staged + `tsc --noEmit`) and `lint-staged` in `package.json`.

6. **Run lint with auto-fix:** `npm run lint:fix`

7. **Fix remaining issues manually** — ESLint reports unfixable violations with
   file + line. Common unfixable: missing JSDoc, `no-explicit-any` in source code,
   import ordering.

8. **Verify clean:** `npm run lint` should report no errors.

9. **Run type check:** `npm run typecheck` — fix any TypeScript errors using the
   [common strict-mode patterns](#common-strict-mode-fix-patterns) above.

10. **Run full gate:** `npm run check` — lint, type-check, and tests must all pass.

11. **Commit:** `chore(lint): add ESLint flat config, JSDoc rules, and TypeScript strict mode`
