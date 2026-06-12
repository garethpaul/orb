# Changes

## 2026-06-12

- Disabled checkout credential persistence in the pinned, read-only hosted
  validation job and added structural checks for that boundary.
- Corrected `planar.DistanceFromWithIndex` for polygons to return the matching
  ring index instead of an outer or hole segment index.
- Added outer-ring, hole-ring, and empty-polygon regression coverage.

## 2026-06-09

- Made planar containment helpers treat empty rings and polygons as
  non-containing inputs instead of panicking.
- Covered `Bound.Union` empty argument behavior so empty bounds stay identity
  values on both sides of union operations.
- Added stable Make aliases for lint, build-through-test, and verify gates.
- Made multipolygon simplification skip empty polygon entries without panicking.
- Clarified and tested that zero-area bounds remain valid while malformed
  negative bounds are empty.

## 2026-06-10

- Added direct coverage that `MultiPolygon.Bound` skips leading empty polygons
  when aggregating child bounds.
- Added the Go race detector to the canonical verification gate.
- Added pinned hosted Linux validation on Go 1.20.14 and Go 1.25.3.
- Pinned checkout to its Node.js 24-compatible release before the hosted
  Node.js 20 action runtime removal.
- Guarded empty line strings in `resample.ToInterval` before distance
  precomputation and callback execution.

## 2026-06-08

- Added a Go module for the existing `github.com/paulmach/orb` import path.
- Pinned the protobuf and error helper dependencies used by MVT encoding.
- Added `make check` and static baseline verification.
- Added `go vet ./...` to the `make check` verification gate.
- Guarded degenerate rings so short rings are not treated as closed and
  orientation checks return zero instead of panicking.
- Made `LineString.Reverse` tolerate empty line strings without panicking.
- Made `Collection.Dimensions` skip nil geometries instead of panicking.
- Made `Bound.Union` treat an empty receiver as an identity value.
- Added local ignore rules for secrets, logs, Go test binaries, coverage
  output, and temporary build artifacts.
- Documented the module path, Mapbox Vector Tile generated source, and testdata
  baseline.
