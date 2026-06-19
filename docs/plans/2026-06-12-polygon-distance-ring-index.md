# Polygon Distance Ring Index

status: completed

## Context

`planar.DistanceFromWithIndex` documents the returned index as the matching
sub-geometry. Multi-geometries and collections return the immediate child
index, but polygon distance currently initializes the result with the outer
ring's matching segment index and shadows the ring loop variable for holes.
Callers therefore receive a segment index instead of the matching polygon ring
index.

## Objectives

- Return ring index `0` when the outer polygon boundary is nearest.
- Return the matching hole ring index when an interior ring is nearest.
- Preserve `+Inf` and `-1` for empty polygons.
- Preserve all distance calculations and immediate-child index behavior for
  other geometry types.
- Add regression tests whose nearest segments differ from the expected ring
  indices so the old behavior cannot pass accidentally.
- Extend maintenance documentation and the baseline checker for the corrected
  public contract.

## Scope Boundaries

- Do not change point-to-segment distance calculations.
- Do not change containment, area, centroid, simplification, or resampling
  behavior.
- Do not alter dependency or Go compatibility declarations.
- Do not modify the occupied PR #1 branch.

## Work Completed

- Returned outer ring index `0` instead of its nearest segment index.
- Returned the matching hole ring index without shadowing the ring loop index.
- Preserved `+Inf` and `-1` for empty polygons.
- Added focused outer, hole, and empty-polygon regression tests.

## Verification Completed

- `GOTOOLCHAIN=go1.20.14 go test ./planar` passed on 2026-06-12.
- `GOTOOLCHAIN=go1.20.14 make check` passed, including race detection and vet,
  on 2026-06-12.
- `GOTOOLCHAIN=go1.25.3 make check` passed, including race detection and vet,
  on 2026-06-12.
- Focused tests rejected mutations restoring the outer-ring segment index and
  the hole-loop segment-index shadowing on 2026-06-12.
- `git diff --check` passed on 2026-06-12.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- Canonical push run `27398396811` and pull-request run `27398401926`
  completed successfully at exact head
  `dd2af0a49a33303c9336f67da7a39ac1c90a42f7` across Go `1.20.14`
  and Go `1.25.3`.
- `TestDistanceFromWithIndex_PolygonReturnsRingIndex` preserves
  `outer ring nearest on nonzero segment` with `index: 0` and
  `hole ring nearest on different segment` with `index: 1`.
- `TestDistanceFromWithIndex_EmptyPolygon` preserves `+Inf` and `-1`.
