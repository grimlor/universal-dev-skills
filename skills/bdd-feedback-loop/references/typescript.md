# TypeScript Feedback Loop Reference

Language-specific guidance for applying `bdd-feedback-loop` in TypeScript projects.

## Step 4 Validation Commands

1. Run editor diagnostics on the test file.
2. Run `tsc --noEmit` on the project (or the specific test file if supported).
3. Run `eslint` on the test file.
4. Run Jest for the targeted test file.

```bash
npx tsc --noEmit
npx eslint src/ tests/
npx jest path/to/test-file.test.ts
```

## Common TypeScript Remediation Issues

- Missing imports (module not found, named export typos)
- Type mismatches -- especially `string | undefined` vs `string` in mock returns
- `any` leaking from mock setup -- use `jest.MockedFunction<typeof fn>` for typed mocks
- Async/sync mock mismatches -- `mockResolvedValue` vs `mockReturnValue`
- Missing `await` on async assertions (causes silent pass)

## Step 5 TypeScript-Specific Checks

- Use `expect(value).toBeCloseTo(expected, precision)` for floating-point comparisons.
- Validate error message content, not only error type -- use `toThrow('expected message')`.
- Avoid `any` in assertions -- if the SUT returns a typed value, assert on typed properties.
- Ensure mock boundaries use `jest.MockedFunction` or `jest.mocked()` for type safety.
