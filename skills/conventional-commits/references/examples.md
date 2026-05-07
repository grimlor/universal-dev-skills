# Conventional Commit Examples

Worked examples covering common types, scopes, bodies, and breaking-change footers. The canonical rules live in `SKILL.md`; this file is illustrative.

## Feature with body and issue link

```
feat(auth): add OAuth2 token refresh

Access tokens now refresh automatically when they expire within
5 minutes of a request. This prevents 401 errors during long
running operations without requiring manual re-authentication.

Refs: #42
```

## Fix with body

```
fix(api): handle missing query parameter without crashing

Previously, an empty `filter` parameter caused a TypeError in
the query builder. Now it defaults to an empty dict and logs
a warning.
```

## CI / release tooling

```
ci(release): add semantic-release workflow

Automates version bumping and GitHub Release creation on push to
main. Reads conventional commit history since the last tag and
determines the appropriate semver increment.
```

## Docs-only change

```
docs: update README with installation instructions
```

## Test addition

```
test(models): add input validation assertions
```

## Dependency bump with breaking change

```
build(deps): bump fastapi from 0.109.0 to 0.110.0

BREAKING CHANGE: 0.110.0 removes the deprecated `on_event`
lifecycle hook. All startup handlers have been migrated to
`lifespan` context managers.
```

## Breaking change via `!` shorthand

```
feat!: redesign workflow format

Step headers now use `####` instead of `###`. Existing workflows
must be updated.
```

Both `!` and a `BREAKING CHANGE:` footer trigger a major bump. `!` is shorter for simple cases; the footer is required when the description alone cannot convey the migration path.
