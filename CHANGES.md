# Changes

## 2026-06-08

- Added a Go module for the existing `github.com/paulmach/orb` import path.
- Pinned the protobuf and error helper dependencies used by MVT encoding.
- Added `make check` and static baseline verification.
- Added `go vet ./...` to the `make check` verification gate.
- Guarded degenerate rings so short rings are not treated as closed and
  orientation checks return zero instead of panicking.
- Made `LineString.Reverse` tolerate empty line strings without panicking.
- Made `Collection.Dimensions` skip nil geometries instead of panicking.
- Added local ignore rules for secrets, logs, Go test binaries, coverage
  output, and temporary build artifacts.
- Documented the module path, Mapbox Vector Tile generated source, and testdata
  baseline.
