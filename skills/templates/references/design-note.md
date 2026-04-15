# Design Note -- <Feature Name>

## Context
What prompted this design? Link to the spec document and summarize the
key requirements that drive architectural choices.

## Component Structure
What are the pieces and how do they relate? List modules, classes, or
packages introduced or modified, and their responsibilities.

<!-- Use a diagram, bullet hierarchy, or prose -- whichever communicates
     the structure most clearly. -->

## Dependency Direction
Which components know about which others? Call out:
- What depends on what (and what must NOT depend on what)
- Interface/protocol boundaries between layers
- Where dependency injection or inversion applies

## I/O Boundaries
Where does the system touch the outside world? Identify every port:
- File system, network, database, external service calls
- Which adapter handles each port
- Where mocks will be injected during testing (must align with spec MOCK BOUNDARY)

## Key Decisions
Why this structure and not the obvious alternative? For each non-trivial
choice, state:
- **Decision:** what was chosen
- **Alternative considered:** what was rejected
- **Rationale:** why -- in terms of the spec requirements, not personal preference

## Trivial Design
<!-- If this feature follows an established pattern in an existing module,
     replace everything above with a single line:

     Follows existing pattern in `<module>`. No new boundaries, interfaces,
     or dependency direction changes.

     The phase still completes -- it just completes quickly. -->
