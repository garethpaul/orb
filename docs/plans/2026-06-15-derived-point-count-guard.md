# Derived Point Count Guard

status: completed

## Summary

Return a controlled nil result when a finite positive resampling interval
produces a nonfinite or integer-overflowing derived point count.

## Problem

`ToInterval` validates the interval itself, then computes `total / dist` and
converts that quotient to `int`. With `planar.Distance`, a finite interval such
as `math.SmallestNonzeroFloat64` makes the quotient overflow to positive
infinity; conversion yields an invalid count and `resample` panics while
allocating its output slice.

## Requirements

- Validate the derived quotient before integer conversion or allocation.
- Return nil for nonfinite or platform-`int`-overflowing point counts.
- Preserve existing finite, representable interval behavior.
- Keep interval validation before distance callback invocation.
- Add focused regression, static, mutation, and maintenance evidence.

## Implementation

- Compute the quotient separately and reject NaN, infinity, or values that
  cannot leave room for the final `+1` point.
- Convert only a validated quotient to the requested point count.
- Add a built-in planar-distance regression using the smallest positive
  floating-point interval.

## Verification

- Run focused resample tests and full `make check` from repository and external
  directories under the maintained Go lanes.
- Reject mutations that remove quotient validation, move conversion before the
  guard, remove the regression or documentation, or leave plan evidence
  incomplete.
- Run module verification, build, vulnerability, diff, artifact, and secret
  audits without changing dependencies or generated code.

## Risks

- This guard does not impose a new general output-size limit on large but
  representable requests; callers remain responsible for practical intervals.
- The change must remain stacked on PR #8 and must not be merged or closed
  without explicit owner authorization.

## Work Completed

- Validated the derived `total / dist` quotient before integer conversion.
- Rejected NaN, infinity, and values that cannot leave room for the final
  point in the platform `int` range.
- Added a smallest-positive-interval regression, ordering contracts, and
  consistent maintenance guidance.

## Verification Completed

- Focused `TestToIntervalRejectsUnrepresentablePointCount` and nonfinite
  interval tests passed under Go 1.20.14 and Go 1.25.11.
- `GOTOOLCHAIN=go1.20.14 make check` and
  `GOTOOLCHAIN=go1.25.11 make check` passed tests, race tests, vet, and the
  static baseline; the external working directory gate also passed.
- `go mod verify` and `go build ./...` passed under both maintained lanes.
- `govulncheck ./...` under Go 1.25.11 reported no vulnerabilities using the
  existing cached tool binary.
- Six isolated hostile mutations removing quotient finiteness, ordering,
  platform integer bounds, regression coverage, guidance, or completed plan
  status were rejected.
- `git diff --check`, exact-diff, generated-artifact, conflict-marker,
  intended-path, dependency/generated-code, binary/large-file, and changed-line
  credential audits passed.
