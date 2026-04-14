# Java Feedback Loop Reference

Language-specific guidance for applying `bdd-feedback-loop` in Java projects.

## Step 4 Validation Commands

1. Run editor diagnostics on the test file.
2. Compile the test sources to catch type errors.
3. Run JUnit 5 for the targeted test class.

```bash
# Gradle
./gradlew classes testClasses
./gradlew test --tests "com.example.MyServiceTest"

# Maven
./mvnw test-compile
./mvnw test -Dtest=MyServiceTest
```

## Common Java Remediation Issues

- Missing imports (IDE may not auto-import AssertJ static methods)
- Wrong argument types passed to constructors -- Java has no named parameters,
  so argument order errors are common
- Unchecked cast warnings in mock setup -- use `@SuppressWarnings("unchecked")`
  with justification if unavoidable
- `when(...).thenReturn(...)` type mismatch -- return type must match the
  stubbed method's signature exactly
- Forgetting `@ExtendWith(MockitoExtension.class)` -- `@Mock` annotations
  won't initialize without it

## Step 5 Java-Specific Checks

- Use `assertThat(value).isCloseTo(expected, within(tolerance))` for
  floating-point comparisons (AssertJ).
- Validate exception message content, not only exception type -- use
  `assertThatThrownBy(...).hasMessageContaining("expected")`.
- Ensure `@Nested` test classes have `@DisplayName` for BDD-style readability.
- Verify strict stubbing -- Mockito's `MockitoExtension` fails on unused stubs
  by default. Remove stubs that aren't exercised.
