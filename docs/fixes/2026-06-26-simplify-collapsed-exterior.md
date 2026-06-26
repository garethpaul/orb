# Fix: Drop Collapsed Simplified Polygons

**Date:** 2026-06-26
**Status:** Fixed
**Severity:** High
**Commit:** This change
**Investigation Tier:** STANDARD with direct-review graceful degradation

## Problem

Direct polygon simplification could return a two-point exterior ring after a
high-threshold reduction, while multipolygon simplification dropped the same
invalid geometry.

## Root Cause

The shared polygon helper filtered collapsed interior rings but exempted ring
zero. The multipolygon wrapper applied a second exterior-length check that the
direct polygon API did not have.

## Solution

Return an empty polygon as soon as the simplified exterior has two or fewer
points. Keep the existing compaction behavior for collapsed interior rings.

## Files Modified

- `simplify/helpers.go` — enforce exterior validity in the shared helper.
- `simplify/helpers_test.go` — cover collapsed exteriors and interior ownership.
- `scripts/check-baseline.py` — preserve implementation and evidence contracts.
- Repository guidance and plans — document the public malformed-geometry boundary.

## Testing

- RED reproduced on Go 1.20.14.
- Full `make check` and `go mod verify` passed on Go 1.20.14 and Go 1.25.11.
- Three isolated hostile mutations were rejected.

## Review Results

- Correctness: approved by direct exact-diff review.
- Quality: approved; the fix stays in the shared helper.
- Security: approved; malformed polygon output fails closed.

## Impact

All simplifier implementations now share consistent direct `Polygon` and
`MultiPolygon` handling when an exterior ring collapses.
