# Negative Callback Segment Distance Guard

Status: planned

## Problem

Resampling rejects a negative derived point count, but that only catches cases
where callback distances sum to a negative total. A callback can return a
negative finite distance for one segment and a larger positive distance for a
later segment. The positive total then reaches interpolation with invalid
cumulative geometry.

## Scope

- Reject each negative finite callback segment before accumulation.
- Apply the shared guard to both `Resample` and `ToInterval` through
  `precomputeDistances`.
- Preserve zero-length segments, positive finite distances, non-finite and
  cumulative-overflow guards, point-count validation, and short-line behavior.
- Add both-entry-point regression coverage, mutation-sensitive static
  contracts, and synchronized guidance.

## Verification

- Run focused resample tests and the full check on Go 1.20.14 and Go 1.25.11.
- Run module verification, builds, and the canonical external-directory check
  on both lanes with explicit timeouts.
- Reject isolated mutations for missing segment validation, either public
  regression, missing guidance, and stale plan status.
- Audit gofmt, exact diff, generated artifacts, dependencies, generated code,
  credentials, conflicts, modes, binaries, and intended paths.

## Risks

- Go 1.20 is end-of-life but remains the intentional compatibility baseline.
- Large positive output requests remain caller-controlled.
- The change must remain stacked on PR #11; neither pull request may be merged
  or closed without explicit owner authorization.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and verification.
