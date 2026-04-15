# Spec -- <Feature Name>

## Overview
One paragraph: what this feature does and why it exists.

## Out of Scope
Explicit list of what this feature does NOT do.

## Public API Surface
<!-- New symbols this feature will expose:
     ClassName(param: Type, ...) -> ReturnType
     module_function(param: Type) -> ReturnType -->

## Behaviors

### <BehaviorName>
REQUIREMENT: <one sentence>
WHO: <who depends on this behavior>
WHAT: <what the behavior does, observable from outside>
WHY: <why is this requirement important? what happens if it's not met?>

MOCK BOUNDARY:
    Mock:  <what to stub -- external I/O, third-party services>
    Real:  <what must be real -- our domain logic, internal components>
    Never: <what must never be mocked -- the system under test>

Scenarios:
- Given <precondition> / When <action> / Then <outcome>

<!-- Repeat the Behaviors section for each distinct behavioral requirement.
     Each behavior should map to one test class in Phase 6. -->
