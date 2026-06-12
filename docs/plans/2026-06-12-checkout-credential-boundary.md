# Checkout Credential Boundary

status: completed

## Context

The exact evidence head still uses the checkout action's default credential
persistence. The Go matrix only needs read access to repository contents.

## Objectives

- Disable checkout credential persistence without changing geometry behavior.
- Enforce one workflow, one read-only permission block, one checkout action,
  and one correctly nested non-persisted credential declaration.
- Preserve immutable action pins, Go 1.20.14 and 1.25.3 lanes, Ubuntu 24.04,
  timeout, concurrency, `GOTOOLCHAIN=local`, and `make check`.
- Correct documentation to match the exact workflow.

## Implementation Units

### Workflow And Checker

Files: `.github/workflows/check.yml` and `scripts/check-baseline.py`.

Add the checkout boundary and reject duplicate workflows, permissions,
checkout actions, write scopes, misplaced or contradictory settings, and
incomplete plan evidence.

### Documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, and this plan.

Record the shorter credential lifetime while preserving the two-version Go
matrix and race-enabled canonical gate.

## Work Completed

- Added `persist-credentials: false` beneath the sole pinned checkout step.
- Added exact workflow, permission, checkout, nesting, contradiction, and plan
  evidence contracts to `scripts/check-baseline.py`.
- Updated hosted-validation documentation without changing Go sources, tests,
  fixtures, generated code, modules, sums, or geometry behavior.

## Verification Completed

- `python3 scripts/check-baseline.py`
- `make lint`, `make test`, `make build`, `make verify`, and `make check`
- workflow YAML parse and `git diff --check`
- Hostile workflow and plan mutations

The local gate retains the race detector and fixed Go 1.20.14/1.25.3 hosted
matrix contract. Canonical hosted push and pull-request checks remain required
at the exact successor head before owner merge.

## Boundaries

- Do not change Go sources, tests, fixtures, generated code, modules, sums, or
  geometry behavior.
- Do not weaken the race detector or either fixed Go lane.
- Preserve the existing remediation PR and exact evidence.
