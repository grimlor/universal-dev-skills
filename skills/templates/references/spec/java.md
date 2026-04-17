# Spec Behavior Example -- Java

JUnit 5 + AssertJ with Javadoc contract and nested test stubs.

```java
/**
 * REQUIREMENT: <one sentence>
 *
 * <p>WHO: <who depends on this behavior>
 * <p>WHAT: (1) <first testable claim -- one observable behavior>.
 *          (2) <second testable claim>.
 *          (3) <third testable claim>.
 * <p>WHY: <why is this requirement important? what happens if it's not met?>
 *
 * <p>MOCK BOUNDARY:
 *     Mock:  <what to stub -- external I/O, third-party services>
 *     Real:  <what must be real -- our domain logic, internal components>
 *     Never: <what must never be mocked -- the system under test>
 */
@DisplayName("<BehaviorName>")
class <BehaviorName>Test {

    /**
     * Given <precondition>
     * When <action>
     * Then <outcome>
     */
    @Test
    @DisplayName("<scenario_proving_what_1>")
    void scenarioProvingWhat1() {
        // Given:

        // When:

        // Then:
        fail("not implemented");
    }

    /**
     * Given <precondition>
     * When <action>
     * Then <outcome>
     */
    @Test
    @DisplayName("<scenario_proving_what_2>")
    void scenarioProvingWhat2() {
        // Given:

        // When:

        // Then:
        fail("not implemented");
    }

    /**
     * Given <precondition>
     * When <action>
     * Then <outcome>
     */
    @Test
    @DisplayName("<scenario_proving_what_3>")
    void scenarioProvingWhat3() {
        // Given:

        // When:

        // Then:
        fail("not implemented");
    }
}
```
