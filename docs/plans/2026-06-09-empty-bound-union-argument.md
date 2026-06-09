# Empty Bound Union Argument Plan

status: completed

## Context

`Bound.Union` treated an empty argument as an identity value, but that branch was
only protected indirectly. A future refactor could remove the `other.IsEmpty`
guard without a focused regression failure.

## Objectives

- Add a direct regression test for empty argument union behavior.
- Extend static checks so `Bound.Union` must keep both empty-side identity
  cases covered.
- Document empty union arguments as part of the aggregate-bound edge-case
  baseline.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
