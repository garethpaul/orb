# Zero Callback Total Guard

Status: completed

## Problem

`Resample` accepts caller-provided distance functions. When a callback returns
zero for every segment of a geometrically non-degenerate line, the target and
segment distances remain zero and the interpolation loop cannot make progress.

## Scope

- Reject an all-zero callback-derived total before interpolation in `Resample`.
- Preserve mixed zero-length and positive callback segments.
- Preserve `ToInterval`, same-point line, positive-distance, negative-distance,
  and non-finite-distance behavior.
- Add regression coverage, a mutation-sensitive static contract, and
  synchronized guidance.

## Verification

- Run focused resample tests and the full check on Go 1.20.14 and Go 1.25.11.
- Run module verification, builds, and the canonical external-directory check
  on both lanes with explicit timeouts.
- Reject isolated mutations for the missing total guard, missing regressions,
  missing guidance, and stale plan status.
- Audit gofmt, exact diff, generated artifacts, dependencies, generated code,
  credentials, conflicts, modes, binaries, and intended paths.

## Risks

- Zero-length segments mixed with positive segments remain valid and must not
  be rejected individually.
- `ToInterval` already resolves a zero total to a one-point result and must not
  change.
- The change must remain stacked on PR #12; neither pull request may be merged
  or closed without explicit owner authorization.

## Work Completed

- Rejected an all-zero callback-derived total before `Resample` enters its
  interpolation loop.
- Added regressions for all-zero rejection and continued support for mixed
  zero-length and positive callback segments.
- Added a mutation-sensitive static contract and synchronized project
  guidance.

## Verification Completed

- Focused resample tests and full tests passed on Go 1.20.14 and Go 1.25.11.
- Race, vet, `go build ./...`, and `go mod verify` passed on both pinned lanes.
- Full `make check` and the absolute-Makefile check from an external working directory
  passed on both pinned lanes.
- Six isolated hostile mutations were rejected for the missing or weakened total
  guard, either public regression, missing guidance, and stale plan status.
- Gofmt, exact diff, artifact, dependency/generated-code, credential,
  conflict-marker, binary, mode, whitespace, and intended-path audits passed.
