# Collection Clip Fixture

Status: Completed

## Context

The clipping suite passed every empty geometry through a no-panic smoke loop,
but did not assert the public result when a nested collection mixed an empty
line string, an inside point, and an outside point.

## Decision

- Clip a nested collection through the public `Geometry` helper.
- Require empty and outside children to be omitted recursively.
- Require the single surviving point to be returned directly rather than
  wrapped in one or more single-element collections.
- No production source change was required because the existing recursive
  collection normalization already satisfies the contract.

## Verification

- Focused `go test ./clip`, full `make check`, and `go mod verify` passed with
  Go 1.20.14 and Go 1.25.11.
- Full gates included all packages, Linux/386 WKB tests, race tests, vet,
  workflow/static contracts, and Make-root isolation.
- Four isolated hostile mutations were rejected for the regression name,
  README recursion and normalization guidance, and plan status.
- `git diff --check` passed.

## Residual Risk

This fixture covers deterministic point survival and empty-child removal. More
complex clipped child types and multiple surviving children retain their
existing package coverage and should receive separate fixtures when changed.
