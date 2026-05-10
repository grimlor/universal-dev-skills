# Refactor Adaptation Plan -- <Refactor Name>

## Audit Summary

Overall audit result: PASS / VIOLATIONS FOUND (delete one)

If violations were found, summarize what was remediated before analysis began. If clean, note "No violations found."

## Per-Class Adaptation Record

<!-- One section per test class that exercises code touched by this refactor. Classes that exercise unaffected code are omitted. -->

### <TestClassName>

**Audit result:** PASS / REMEDIATED (note what was fixed if remediated)

**Current mock boundary:** <!-- What concrete type or interface is currently being substituted in this class -->

**New mock boundary:** <!-- What new Protocol, port, or adapter shape the fake must conform to after the refactor -->

**Fixture changes:**

<!-- List fakes to create or update. For each, state:
     - Name of the fake
     - New interface it must conform to (method signatures, return types)
     - Whether it is a new fake or an update to an existing one -->

**Behavioral assertions:** UNCHANGED / WORDING UPDATE NEEDED / NEW FAILURE MODE

<!-- If unchanged: note that WHAT clauses and assertion bodies are valid under the new interface as-is.
     If wording update needed: describe the specific wording change and confirm it is not a behavioral change.
     If new failure mode: this is the exception case -- describe the failure mode the new interface exposes
     that the old interface could not produce. -->

**New test methods required:**

<!-- Only populated when "NEW FAILURE MODE" above. For each new method:
     - Method name (behavior statement, not implementation description)
     - Given / When / Then scenario
     Leave blank or write "None" if behavioral assertions are unchanged. -->

<!-- Repeat ### section for each affected test class -->

## Design Gaps Identified

<!-- Any gaps discovered during analysis that triggered a retreat to Phase 2 design, and their resolutions. Leave blank or write "None" if no gaps were found. -->

## Open Questions

<!-- Anything unresolved that requires user input before Phase 4 can begin. -->
