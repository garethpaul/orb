# Make Gate Aliases Plan

status: completed

## Context

`orb` already had a repeatable `make check` gate for Go tests, Go vet, and
static baseline verification. Several automation surfaces also expect common
project aliases such as `make lint`, `make build`, and `make verify`.

## Objectives

- Add `make lint` as the stable alias for `go vet ./...`.
- Add `make build` as the library build-through-test alias.
- Add `make verify` as the stable full verification alias.
- Extend static baseline checks and docs so the aliases remain discoverable.

## Verification

- `make lint`
- `make build`
- `make verify`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
