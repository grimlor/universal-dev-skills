# Spec Behavior Example -- C#

xUnit + FluentAssertions with XML doc contract and nested test stubs.

```csharp
/// <summary>
/// REQUIREMENT: <one sentence>
///
/// WHO: <who depends on this behavior>
/// WHAT: (1) <first testable claim -- one observable behavior>.
///       (2) <second testable claim>.
///       (3) <third testable claim>.
/// WHY: <why is this requirement important? what happens if it's not met?>
///
/// MOCK BOUNDARY:
///     Mock:  <what to stub -- external I/O, third-party services>
///     Real:  <what must be real -- our domain logic, internal components>
///     Never: <what must never be mocked -- the system under test>
/// </summary>
public class <BehaviorName>Tests
{
    /// <summary>
    /// Given <precondition>
    /// When <action>
    /// Then <outcome>
    /// </summary>
    [Fact]
    public void Scenario_proving_what_1()
    {
        // Given:

        // When:

        // Then:
        throw new NotImplementedException();
    }

    /// <summary>
    /// Given <precondition>
    /// When <action>
    /// Then <outcome>
    /// </summary>
    [Fact]
    public void Scenario_proving_what_2()
    {
        // Given:

        // When:

        // Then:
        throw new NotImplementedException();
    }

    /// <summary>
    /// Given <precondition>
    /// When <action>
    /// Then <outcome>
    /// </summary>
    [Fact]
    public void Scenario_proving_what_3()
    {
        // Given:

        // When:

        // Then:
        throw new NotImplementedException();
    }
}
```
