# Polygon Distance Ring Index

status: planned

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

## Verification

- `GOTOOLCHAIN=go1.20.14 go test ./planar`
- `GOTOOLCHAIN=go1.20.14 make check`
- `GOTOOLCHAIN=go1.25.3 make check`
- Mutations restoring outer-ring segment indices or hole-loop shadowing are
  rejected by focused tests and the baseline.
- `git diff --check`
