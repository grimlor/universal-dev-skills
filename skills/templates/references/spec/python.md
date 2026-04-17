# Spec Behavior Example -- Python

pytest class with docstring contract and method stubs.

```python
class Test<BehaviorName>:
    """
    REQUIREMENT: <one sentence>

    WHO: <who depends on this behavior>
    WHAT: (1) <first testable claim -- one observable behavior>.
          (2) <second testable claim>.
          (3) <third testable claim>.
    WHY: <why is this requirement important? what happens if it's not met?>

    MOCK BOUNDARY:
        Mock:  <what to stub -- external I/O, third-party services>
        Real:  <what must be real -- our domain logic, internal components>
        Never: <what must never be mocked -- the system under test>
    """

    def test_<scenario_proving_what_1>(self):
        """
        Given <precondition>
        When <action>
        Then <outcome>
        """
        ...

    def test_<scenario_proving_what_2>(self):
        """
        Given <precondition>
        When <action>
        Then <outcome>
        """
        ...

    def test_<scenario_proving_what_3>(self):
        """
        Given <precondition>
        When <action>
        Then <outcome>
        """
        ...
```
