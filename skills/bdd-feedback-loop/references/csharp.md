# C# Feedback Loop Reference

Language-specific guidance for applying `bdd-feedback-loop` in C# projects.

## Step 4 Validation Commands

1. Run editor diagnostics on the test file.
2. Build the solution to catch compiler errors and analyzer warnings.
3. Run xUnit for the targeted test class.

```bash
dotnet build --warnaserrors
dotnet test --filter "FullyQualifiedName~MyServiceTests"
```

## Common C# Remediation Issues

- Nullable reference type warnings (`CS8600`, `CS8602`) -- use `!` only with
  justification, prefer null guards or `?` chaining
- Missing `using` directives (FluentAssertions, Moq, xUnit)
- `Setup` vs `Returns` type mismatch -- Moq's `Returns()` must match the
  mocked method's return type exactly
- Forgetting `async Task` return type on async test methods -- xUnit silently
  ignores `async void` tests
- Constructor parameter order errors -- C# has no keyword arguments in most
  cases, so order matters

## Step 5 C#-Specific Checks

- Use `value.Should().BeApproximately(expected, precision)` for floating-point
  comparisons (FluentAssertions).
- Validate exception message content, not only exception type -- use
  `.WithMessage("*expected*")`.
- Ensure nested test classes follow BDD grouping conventions (see
  `bdd-testing/references/csharp.md` for xUnit patterns).
- Verify mock behavior -- use `MockBehavior.Strict` when you want to catch
  unexpected interactions.
