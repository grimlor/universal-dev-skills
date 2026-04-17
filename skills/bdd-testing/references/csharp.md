# C# BDD Reference

Language-specific guidance for applying `bdd-testing` in C# projects.

## I/O Boundary Examples

| I/O boundary (mock these) | Part of the system (never mock) |
|---|---|
| `Process.Start()` -- spawns a process | `RepoDiscovery.Discover()` -- our method that calls Process |
| `HttpClient.SendAsync()` -- HTTP call | `DetailsFetcher.FetchAsync()` -- our method that calls HttpClient |
| `DbConnection.ExecuteReader()` -- database wire call | `RepoRepository.FindById()` -- our caching/query logic |
| `Directory.GetCurrentDirectory()` -- process-level state | `File.Exists(path)` with temp dir -- use real filesystem instead |

Use `Path.Combine(Path.GetTempPath(), Path.GetRandomFileName())` or a test
helper to create real temp directories so that `File.Exists`, `Directory.Exists`,
and `Directory.GetFiles` all run against real filesystem structure.

## Coverage Commands

```bash
# Run tests with coverage collection
dotnet test --collect:"XPlat Code Coverage"

# Run with coverage threshold enforcement (100% for personal projects)
dotnet test --collect:"XPlat Code Coverage" \
    /p:CollectCoverage=true \
    /p:Threshold=100 \
    /p:ThresholdType=line \
    /p:ThresholdStat=total
```

For forked or contributed projects, match the upstream's threshold.

## Test Structure -- xUnit + FluentAssertions

```csharp
using FluentAssertions;
using Moq;
using Xunit;

public class RetryPolicyTests
{
    public class WhenMaxRetriesReached
    {
        [Fact]
        public void Should_throw_RetryExhaustedException()
        {
            var policy = new RetryPolicy(maxRetries: 3, baseDelay: TimeSpan.FromMilliseconds(10));

            var act = () => policy.ExecuteWithRetries(() => throw new IOException("fail"));

            act.Should().Throw<RetryExhaustedException>()
                .WithMessage("*3 retries*");
        }
    }
}
```

Use nested classes for BDD-style "context" grouping. xUnit's `[Fact]` and
`[Theory]` attributes serve as specifications -- no separate display-name
annotation is needed.

## Exception Assertion Patterns

```csharp
// FluentAssertions -- preferred
var act = () => ParseConfig(null);
act.Should().Throw<ArgumentNullException>()
    .WithMessage("*must not be null*");

// FluentAssertions -- async
var act = async () => await service.ProcessAsync(invalidInput);
await act.Should().ThrowAsync<ValidationException>()
    .WithMessage("*invalid*");

// xUnit -- when you only need the exception type
Assert.Throws<ArgumentNullException>(() => ParseConfig(null));
```

Always assert the error message, not just the exception type -- this prevents
tests from passing on the wrong exception.

## Async Test Patterns

```csharp
// Async/await (preferred)
[Fact]
public async Task Should_fetch_data()
{
    var result = await service.GetDataAsync();
    result.Should().NotBeNull();
}

// Async exception assertion
[Fact]
public async Task Should_reject_bad_input()
{
    var act = async () => await service.ProcessAsync(null);
    await act.Should().ThrowAsync<ArgumentNullException>();
}
```

Always `await` the assertion -- an un-awaited async assertion will silently
pass.

## Mock Boundary Patterns

```csharp
public class OrderServiceTests
{
    private readonly Mock<IPaymentGateway> _paymentGateway = new();
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _sut = new OrderService(_paymentGateway.Object);
    }

    [Fact]
    public void Should_call_payment_gateway_with_correct_amount()
    {
        _paymentGateway
            .Setup(g => g.Charge(It.IsAny<PaymentRequest>()))
            .Returns(PaymentResult.Success());

        _sut.PlaceOrder(new Order(100.0m));

        _paymentGateway.Verify(
            g => g.Charge(It.Is<PaymentRequest>(r => r.Amount == 100.0m)),
            Times.Once);
    }
}
```

Mock at module boundaries (API clients, external services, databases), not
internal classes. See `bdd-testing` core skill for the full mock boundary
contract.

### Strict Mock Behavior

```csharp
// Strict mode -- throws on unexpected calls
var mock = new Mock<IService>(MockBehavior.Strict);
```

Use `MockBehavior.Strict` when you want to ensure no unexpected interactions
occur. Default (`Loose`) is fine for most tests where you only care about
specific interactions.

## Analyzer and Build Verification

After completing test changes, verify with:

```bash
dotnet format --verify-no-changes
dotnet build --warnaserrors
dotnet test --collect:"XPlat Code Coverage"
```

All must pass clean before the tests are considered done.
