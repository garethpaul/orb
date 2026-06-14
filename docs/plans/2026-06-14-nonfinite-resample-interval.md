# Non-Finite Resample Interval Guard

status: planned

## Context

`resample.ToInterval` rejects zero and negative distances, but IEEE-754 `NaN`
and infinity pass that comparison. A non-degenerate line with a `NaN` interval
can therefore reach point-count conversion with a non-finite quotient and panic
instead of returning a controlled result.

## Objectives

- Reject `NaN`, positive infinity, and negative infinity before invoking the
  caller-provided distance function.
- Preserve the existing nil result for zero and negative intervals.
- Preserve current resampling behavior for finite positive intervals.
- Add regression coverage that fails if non-finite values reach distance
  calculation or point-count conversion.
- Extend the static baseline and maintenance guidance for the finite-interval
  contract.

## Scope Boundaries

- Do not change `Resample` point-count behavior or interpolation.
- Do not change how caller-provided distance functions calculate segment
  lengths.
- Do not change the Go compatibility baseline or dependency graph.
- Keep this work stacked on the location-independent Make pull request.

## Implementation Units

1. Add a focused `ToInterval` regression covering `NaN` and both infinities,
   including proof that the distance callback is not invoked.
2. Add the smallest finite-positive interval guard before line edge cases and
   distance precomputation.
3. Extend the static baseline, security guidance, changelog, and this plan's
   completed evidence so the contract cannot regress silently.

## Test Scenarios

- A multi-point line with `NaN` returns nil without panic or distance calls.
- A multi-point line with positive infinity returns nil without distance calls.
- A multi-point line with negative infinity returns nil without distance calls.
- Existing zero, negative, empty, single-point, downsample, and upsample cases
  remain unchanged.

## Verification

- Focused resample tests on Go 1.20.14 and Go 1.25.11.
- Full `make check` on both supported toolchains.
- Absolute-path `make check` from an external working directory.
- Mutation checks for the finite guard, callback-order regression, static
  contract, documentation, and completed plan evidence.
- Final diff, generated-artifact, and high-signal credential audits.
