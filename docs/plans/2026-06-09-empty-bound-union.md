# Empty Bound Union Plan

status: completed

## Context

`Bound.Union` already ignored an empty `other` bound, but did not treat an
empty receiver as an identity value. Aggregate helpers that seeded a union from
an empty child could leak the `emptyBound` sentinel into the final result.

## Objectives

- Make `Bound.Union` return the other bound when the receiver is empty.
- Add a direct regression test for empty receiver union behavior.
- Add a multi-line-string regression where the first child has an empty bound.
- Extend static checks and docs for empty bounds in aggregate helpers.

## Verification

- `make check`
- `go test ./...`
- `git diff --check`
