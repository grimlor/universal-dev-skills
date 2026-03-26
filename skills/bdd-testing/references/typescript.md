# TypeScript BDD Reference

Language-specific guidance for applying `bdd-testing` in TypeScript projects.

## Coverage Commands

```bash
# Jest coverage report
npm run test:coverage
# or directly:
jest --coverage
```

Coverage threshold is enforced in `jest.config.js` at 100% for branches,
functions, lines, and statements in personal projects. For forked or
contributed projects, match the upstream's threshold.

## Exception / Error Assertion Patterns

```typescript
// Synchronous error
expect(() => parseConfig(null)).toThrow('Config must not be null');

// Async error
await expect(fetchData('bad-url')).rejects.toThrow('Failed to fetch');

// Error type + message
expect(() => validate(input)).toThrow(expect.objectContaining({
  message: expect.stringContaining('invalid'),
}));
```

Always assert the error message, not just the error type — this prevents
tests from passing on the wrong `Error`.

## Async Test Patterns

```typescript
// Async/await (preferred)
it('should fetch data', async () => {
  const result = await service.getData();
  expect(result).toBeDefined();
});

// Resolves/rejects matchers
it('should reject on bad input', async () => {
  await expect(service.process(null)).rejects.toThrow();
});
```

Always `await` the assertion or return the promise — an un-awaited async
assertion will silently pass.

## Mock Boundary Patterns

```typescript
// Jest manual mock
jest.mock('../src/api/client', () => ({
  fetchData: jest.fn(),
}));

// Typed mock reference
import { fetchData } from '../src/api/client';
const mockFetchData = fetchData as jest.MockedFunction<typeof fetchData>;

// Per-test setup
mockFetchData.mockResolvedValue({ id: 1, name: 'test' });
```

Mock at module boundaries (API clients, external services, browser APIs),
not internal functions. See `bdd-testing` core skill for the full mock
boundary contract.

## `any` in Tests

ESLint `@typescript-eslint/no-explicit-any` is `off` in `tests/**/*.ts` per
the canonical ESLint config. Use `any` sparingly for mock setup and dynamic
assertions where full typing adds noise without safety.

## Static Analysis Verification

After completing test changes, verify with:

```bash
npm run typecheck    # tsc --noEmit
npm run lint         # eslint .
```

Both must pass clean before the tests are considered done.
