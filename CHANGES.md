# Changes

## 2026-06-25T20:30:44Z — P1 correctness — cycle: maptile zoom boundary

- Threads: inspected the default branch, recent pull requests, hosted checks,
  repository contracts, projection helpers, tile arithmetic, and existing
  boundary coverage; no open pull requests or issues were present.
- Bug fixed: preserved the `2^32` Web Mercator scale instead of narrowing it
  to zero, restoring zoom-32 tile validation, point projection, bounds, and
  scalar Mercator round trips; tile coordinates now clamp before conversion so
  the eastern boundary cannot wrap in direct or tile-cover projection, and
  inclusive bound-cover loops terminate before `uint32` wraparound; zooms above
  the coordinate capacity produce invalid `At` tiles.
- Files: `maptile/tile.go`, `maptile/tile_test.go`,
  `maptile/tilecover/line_string.go`, `maptile/tilecover/cover_test.go`,
  `maptile/tilecover/helpers.go`,
  `internal/mercator/mercator.go`, and `internal/mercator/mercator_test.go`.
- Validation: reproduced four zoom-32 failures on Go 1.20.14, then passed all
  tests, race tests, and vet on Go 1.20.14 and Go 1.25.11 plus static baseline,
  hosted-workflow contract, and Make root contract checks.
- Blockers: the host has no Go executable, so validation used pinned official
  Docker images; no implementation or release blocker remains.
- Next: define compatibility semantics for `Children`, `Range`, and internal
  Mercator calls above the representable tile zoom before changing them.

## 2026-06-21

- Made absolute Makefile verification safe for spaces and apostrophes,
  ignored caller-provided `REPO_ROOT` values, and rejected command-line or
  environment `MAKEFILE_LIST` injection before Go gates run.
- Added root-policy regressions for every public Make target.

## 2026-06-19

- Bounded resampling output allocations to 64 MiB of points and rejected nil
  distance callbacks, non-finite coordinates, and non-progressing sample spacing.
- Switched interpolation to a finite overflow-safe weighted form and added
  deterministic property coverage for point counts, endpoints, and progress.
- Kept polygon distance indices at `-1` when no ring contains a segment.

## 2026-06-15

- Rejected nonfinite or integer-overflowing derived `ToInterval` point counts
  before integer conversion and output allocation.
- Rejected negative derived point counts from invalid distance callbacks before
  conversion and allocation.
- Rejected non-finite callback distances and callback-derived cumulative totals
  before either resampling entry point interpolates or allocates output points.
- Rejected negative callback segment distances before accumulation in both
  resampling entry points.
- Rejected a zero callback total before either resampling path interpolates while
  preserving mixed zero-length and positive callback segments.

## 2026-06-14

- Rejected non-finite `resample.ToInterval` distances before distance callback
  execution or point-count conversion, preventing a `NaN`-driven panic.
- Added regression and static contract coverage for `NaN` and both infinities.

## 2026-06-13

- Made every standard Make gate resolve Go module and checker paths from the
  repository root, including absolute-Makefile calls from external directories.
- Documented the Go 1.20 compatibility minimum, fixed 1.20.14 and patched 1.25.11
  validation roles, local-toolchain boundary, module-path stability,
  dependency-integrity checks, and generated protobuf expectations.

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
