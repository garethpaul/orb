# Negative Derived Point Count Guard

status: completed

## Context

`ToInterval` rejects nonfinite and integer-overflowing derived point counts, but
a caller-provided distance function can return a finite negative total. The
negative quotient survives the guard, converts to a nonpositive point count,
and can panic when used as a slice capacity.

## Goal

Reject negative derived point counts before integer conversion, edge-case
handling, or output allocation while preserving valid finite-positive behavior.

## Scope

- Add a negative quotient guard beside the existing NaN, infinity, and maximum
  integer checks.
- Add a regression using a negative distance callback and require a nil result
  without panic.
- Add mutation-sensitive static contracts and synchronized guidance.
- Do not redefine valid distance metrics or impose a practical allocation cap.

## Verification Plan

- Run the focused resample tests and both maintained Go toolchain lanes.
- Run tests, race tests, vet, builds, module verification, external Make, and
  vulnerability checks.
- Reject isolated source, test, guidance, and plan mutations.
- Audit `git diff --check`, generated artifacts, dependency files, binaries,
  modes, and credential-shaped additions.

## Work Completed

- Rejected negative derived point counts beside the existing nonfinite and
  integer-overflow checks, before conversion or allocation.
- Added a regression using a negative caller distance callback.
- Added mutation-sensitive static contracts and synchronized guidance.

## Verification Completed

- `TestToIntervalRejectsNegativeDerivedPointCount` passed under Go 1.20.14 and
  Go 1.25.11.
- `make check` passed under both maintained lanes, including tests, race tests,
  vet, and the static baseline; the external working directory gate passed.
- `go mod verify` and `go build ./...` passed under both toolchains.
- `GOTOOLCHAIN=go1.25.11 go run golang.org/x/vuln/cmd/govulncheck@latest ./...`
  (`govulncheck ./...`) reported no vulnerabilities.
- Five isolated hostile mutations covering the source guard, test name,
  callback sign, guidance, and plan evidence were rejected.
- `git diff --check` plus generated-artifact, dependency-file, binary, mode,
  credential-shaped addition, and intended-path audits passed.
