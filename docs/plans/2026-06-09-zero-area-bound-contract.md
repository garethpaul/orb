# Zero-Area Bound Contract

status: completed

## Context

`Bound.IsEmpty` treats malformed negative bounds as empty, but preserves
zero-area bounds such as single points and horizontal or vertical segments. The
comment still described zero-area bounds as empty, and the table-driven tests
named those cases without actually constructing zero-area bounds.

## Objectives

- Clarify the `Bound.IsEmpty` comment without changing behavior.
- Update the table tests to use actual single-point, horizontal, and vertical
  zero-area bounds.
- Extend the static baseline and docs for the zero-area bound contract.
- Keep malformed negative bounds covered as empty.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
