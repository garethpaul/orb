# Zero Round Factor Safety

Status: completed

## Problem

`Round` divided every coordinate by the caller-provided factor without first
validating it. A zero factor replaced finite coordinates with `NaN`.
Collection recursion also converted the floating-point factor back through
`int`, coupling nested behavior to an avoidable numeric round trip.

## Scope

- Make an explicit zero factor leave geometry unchanged.
- Apply validation before any slice-backed geometry can be mutated.
- Reuse one floating-point factor throughout nested collections.
- Preserve positive factors, negative-factor equivalence, the mutable default
  factor, and all public types.

## Work Completed

- Added a nested public regression spanning points, line strings, and bounds.
- Proved a zero factor preserves every coordinate exactly.
- Added a pre-mutation zero guard and an internal recursive helper.
- Added a compatibility regression proving negative factors still match their
  positive magnitude.
- Preserved nil collection children through the internal helper rather than
  bypassing the public nil contract.
- Synchronized public, security, roadmap, and maintainer guidance.
- Added fail-closed source, regression, plan, and guidance contracts.

## Verification Completed

- RED focused root-package testing on Go 1.20.14 proved a zero factor replaced
  finite coordinates with `NaN` and a negative factor unexpectedly rounded
  coordinates to integers.
- Focused root-package tests, all-package tests, race tests, vet, full
  `make check`, and `go mod verify` passed in pinned Docker toolchains for
  Go 1.20.14 and Go 1.25.11 because the host has no Go executable installed.
- Twelve isolated hostile mutations were rejected across the guard, recursive
  helper, zero and negative-factor regressions, plan, and synchronized guidance.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.

## Residual Risk

Positive factors can still overflow intermediate multiplication for extreme
finite coordinates or factors. That existing numeric policy is separate from
the zero-input corruption fixed here.
