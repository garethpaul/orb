# Orb Go Module Baseline Plan

status: completed

## Context

`orb` is a Go geometry library with broad test coverage across core geometry
types, clipping, GeoJSON, WKB/WKT, map tiles, projections, quadtrees,
resampling, simplification, and Mapbox Vector Tile encoding.

## Risks

- The repository used the old GOPATH workflow and could not run `go test ./...`
  from this checkout because packages import `github.com/paulmach/orb`.
- External dependencies for generated Mapbox Vector Tile support were implicit.
- There was no local `make check` entry point for repeatable verification.
- Generated binaries, coverage files, and local secrets were not ignored.

## Work Completed

- Added `go.mod` and `go.sum` using the existing import path
  `github.com/paulmach/orb`.
- Pinned the external dependencies already used by the code:
  `github.com/gogo/protobuf` and `github.com/pkg/errors`.
- Added `make check`, `make test`, and static baseline checks.
- Added ignore rules for local secrets, logs, Go test binaries, coverage
  output, and temporary build artifacts.
- Documented the module path, fixture expectations, and verification workflow.

## Verification

- `go test ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
