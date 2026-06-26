# Resample Degenerate Public Fixtures

Status: completed

## Problem

The public resampling test exercised empty and single-point line strings only as
panic smoke checks. Zero-length behavior was distributed across broader safety
tests, leaving the public output contracts for both entry points implicit.

## Scope

- Add focused public fixtures for empty, single-point, and repeated-point lines.
- Prove empty and single-point inputs return before invoking the distance callback.
- Prove `Resample` expands a zero-length line to the requested identical points.
- Prove `ToInterval` collapses a zero-length line to one identical point.
- Preserve implementation and exported behavior unchanged.

## Work Completed

- Added dedicated `Resample` and `ToInterval` degenerate-input regressions.
- Added callback traps, exact output-length checks, and coordinate assertions.
- Added mutation-sensitive static contracts and synchronized maintainer guidance.
- Removed the completed fixture item from the forward roadmap.

## Verification Completed

- RED static baseline verification rejected the missing public fixture names and
  assertions before the tests were added.
- Focused `go test ./resample`, full `make check`, and `go mod verify` passed in
  pinned Docker toolchains for Go 1.20.14 and Go 1.25.11 because the host has no
  Go executable installed.
- Fourteen isolated hostile mutations were rejected across fixture names,
  assertions, guidance, and completed-plan evidence.
- `git diff --check` passed.

## Residual Risk

The fixtures preserve current degenerate behavior but do not validate arbitrary
caller callback consistency. Existing finite-distance, progress, allocation,
and interpolation guards continue to cover that separate risk surface.
