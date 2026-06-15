# Non-Finite Resample Callback Distance

status: planned

## Context

`Resample` trusts every value returned by its distance callback. A `NaN` or
infinite segment distance reaches the point-placement loop, leaves the result
shorter than requested, and can panic during final endpoint assignment.
`ToInterval` rejects a non-finite derived point count, but callback validation
is not shared explicitly between the two entry points.

## Goal

Reject line strings whose distance callback produces a non-finite segment
distance before either resampling path allocates or interpolates output points.

## Scope

- Detect `NaN` and positive or negative infinity while precomputing segment
  distances.
- Return `nil` from `Resample` and `ToInterval` when callback distances are
  non-finite.
- Preserve valid callback behavior, short-line handling, negative-derived-count
  rejection, dependencies, generated code, and supported Go lanes.
- Add no-panic regressions, mutation-sensitive static contracts, synchronized
  guidance, and truthful completed evidence.

## Implementation Units

### U1: Validate precomputed distances

Files: `resample/line_string.go`, `resample/line_string_test.go`

Carry callback validity out of distance precomputation and stop both public
entry points before interpolation when a segment is non-finite.

### U2: Lock the boundary into project verification

Files: `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-15-nonfinite-callback-distance.md`

Require the shared guard, both public-path regressions, synchronized guidance,
and completed verification without changing module or generated-code paths.

## Verification Plan

- Run focused resample tests on Go 1.20.14 and Go 1.25.11.
- Run both full Make validation lanes, module verification, builds, and the
  absolute-Makefile gate from an external directory.
- Reject isolated mutations of callback validation, public-path handling,
  tests, guidance, and completed plan evidence.
- Audit gofmt, the exact diff, generated artifacts, dependency changes,
  credentials, binaries, modes, and unintended paths.

## Scope Boundaries

- Do not impose a new general point-count cap or change valid interpolation.
- Do not redefine negative finite callback distances beyond the existing
  derived-point-count behavior.
