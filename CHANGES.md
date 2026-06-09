# Changes

## 2026-06-09

- Made planar containment helpers treat empty rings and polygons as
  non-containing inputs instead of panicking.
- Covered `Bound.Union` empty argument behavior so empty bounds stay identity
  values on both sides of union operations.
- Added stable Make aliases for lint, build-through-test, and verify gates.
- Made multipolygon simplification skip empty polygon entries without panicking.
- Clarified and tested that zero-area bounds remain valid while malformed
  negative bounds are empty.

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
