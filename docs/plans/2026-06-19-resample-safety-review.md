# Resample Safety Review

Status: completed

## Scope

Review the overlapping remediation root and the linear polygon-distance and
resampling stack through PR #13. Preserve the Go 1.20 API while closing concrete
panic, allocation, floating-point progress, interpolation, and ring-index gaps.

## Root Cause

The original 2019 sampler trusted caller-provided point counts, coordinates,
and distance callbacks. The 2026 stack added interval and callback validation,
but output allocation remained unbounded, a nil callback still panicked,
subnormal totals could produce a zero target spacing and duplicate samples, and
the interpolation expression overflowed for opposite finite extremes. The
polygon ring-index correction initialized its result to ring zero even when no
ring had a segment.

Provenance is clear: the sampler and interpolation loop originate in commit
`594009f`; PRs #8-#13 added the numeric callback guards carried into this review;
commit `dd2af0a` introduced the segmentless polygon index regression while
correcting ordinary outer-ring and hole-ring results.

## Changes

- Cap resampling output to 64 MiB of `orb.Point` values.
- Reject nil callbacks, non-finite coordinates and distances, non-progressing
  spacing, and incomplete sample generation before returning geometry.
- Skip zero-length callback segments while keeping mixed zero/positive segments.
- Use weighted interpolation that remains finite for opposite finite extremes.
- Return `+Inf, -1` when a polygon has no ring segment.
- Add deterministic property-style tests and focused regression tests.
- Integrate the useful contributor guidance from remediation PR #1.

## Verification

- RED observed for nil callback panic, underflow duplicate output, overflowing
  interpolation, unbounded point count, zero callback total in `ToInterval`, and
  segmentless polygon index zero.
- `GOTOOLCHAIN=go1.20.14 go test ./resample ./planar`
- `GOTOOLCHAIN=go1.25.11 go test ./resample ./planar`
- `go vet` for both supported toolchains on `./resample ./planar`
- `python3 scripts/check-baseline.py`
- Six isolated hostile mutations rejected.
- Hosted Linux `make check` passed twice for both Go 1.20.14 and Go 1.25.11 on
  aggregate head `76f86b87f5c3bf02589ac49eb5d9edc8b268ffd9` in runs
  `27845256306` and `27845258511`.
- CodeQL Actions, Go, and Python analysis passed in run `27845257744`.
- Branch protection was updated from the obsolete `test (1.25.3)` context to
  the successful documented `test (1.25.11)` context while retaining strict
  required checks for both supported lanes.

## Residual Risk

The distance callback remains authoritative for segment weighting and can be
geometrically inconsistent while still finite and non-negative. Resampling is
linear in coordinate space, not geodesic, and does not infer ring closure or
polygon topology. The fixed allocation budget intentionally rejects very large
but otherwise representable output requests.

## Native Arm64 Fixture Divergence

Local native `darwin/arm64` runs under Go 1.20.14 and the installed Go 1.26.1
do not satisfy several pre-existing exact floating-point fixtures in
`internal/mercator`, `maptile`, and `simplify`. The same repository state passes
the complete Go 1.20.14 and Go 1.25.11 matrices under `GOARCH=amd64`, including
the race detector. This review does not change those fixtures or claim to fix
their architecture sensitivity; hosted Linux amd64 remains the authoritative
repository gate.
