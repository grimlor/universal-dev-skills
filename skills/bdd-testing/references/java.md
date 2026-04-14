# Java BDD Reference

Language-specific guidance for applying `bdd-testing` in Java projects.

## Coverage Commands

```bash
# Gradle -- run tests and generate coverage report
./gradlew test jacocoTestReport

# Gradle -- verify coverage threshold (fails if below 100%)
./gradlew check

# Maven
./mvnw verify
```

Coverage threshold is enforced at 100% line coverage via JaCoCo's
`jacocoTestCoverageVerification` task in personal projects. For forked or
contributed projects, match the upstream's threshold.

## Test Structure -- JUnit 5 + AssertJ

```java
import static org.assertj.core.api.Assertions.*;
import org.junit.jupiter.api.*;

@DisplayName("RetryPolicy")
class RetryPolicyTest {

    @Nested
    @DisplayName("when max retries is reached")
    class WhenMaxRetriesReached {

        @Test
        @DisplayName("should throw RetryExhaustedException")
        void shouldThrowRetryExhausted() {
            var policy = new RetryPolicy(3, Duration.ofMillis(10));

            assertThatThrownBy(() -> policy.executeWithRetries(() -> {
                throw new IOException("fail");
            }))
                .isInstanceOf(RetryExhaustedException.class)
                .hasMessageContaining("3 retries");
        }
    }
}
```

Use `@Nested` classes for BDD-style "context" grouping and `@DisplayName`
for human-readable specifications.

## Exception Assertion Patterns

```java
// AssertJ -- preferred
assertThatThrownBy(() -> parseConfig(null))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessageContaining("must not be null");

// AssertJ -- capture and inspect
Throwable thrown = catchThrowable(() -> service.process(invalidInput));
assertThat(thrown)
    .isInstanceOf(ValidationException.class)
    .hasMessageContaining("invalid");

// JUnit 5 -- when you only need the exception type
assertThrows(IllegalArgumentException.class, () -> parseConfig(null));
```

Always assert the error message, not just the exception type -- this prevents
tests from passing on the wrong exception.

## Async / Concurrent Test Patterns

```java
// CompletableFuture assertions
assertThatThrownBy(() -> service.fetchAsync("bad-url").join())
    .isInstanceOf(CompletionException.class)
    .hasCauseInstanceOf(IOException.class);

// Timeout for async operations
@Test
@Timeout(value = 5, unit = TimeUnit.SECONDS)
void shouldCompleteWithinTimeout() {
    var result = service.longRunningOp().join();
    assertThat(result).isNotNull();
}
```

## Mock Boundary Patterns

```java
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private PaymentGateway paymentGateway;

    @InjectMocks
    private OrderService orderService;

    @Test
    @DisplayName("should call payment gateway with correct amount")
    void shouldCallPaymentGateway() {
        when(paymentGateway.charge(any()))
            .thenReturn(PaymentResult.success());

        orderService.placeOrder(new Order(100.0));

        verify(paymentGateway).charge(argThat(req ->
            req.getAmount() == 100.0
        ));
    }
}
```

Mock at module boundaries (API clients, external services, databases), not
internal classes. See `bdd-testing` core skill for the full mock boundary
contract.

### Strict Stubbing

Mockito's `MockitoExtension` enables strict stubbing by default -- unused
stubs cause test failures. This is the desired behavior; it prevents dead
mock setup from accumulating.

## Static Analysis Verification

After completing test changes, verify with:

```bash
# Gradle
./gradlew check

# Maven
./mvnw verify
```

This runs tests + coverage verification + Checkstyle + SpotBugs. All must
pass clean before the tests are considered done.
