## Orb Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Orb is a Go geometry library for working with two-dimensional geographic and
planar data.

The repository is useful because it keeps simple geometry types at the center
and layers focused packages around them for GeoJSON, map tiles, clipping,
projection, quadtrees, resampling, simplification, and database-friendly
geometry encodings.

The goal is to keep the core types idiomatic, stable, and easy to compose while
maintaining correctness across geographic and planar operations.

Current baseline: `make check` runs `go test ./...`, `make lint`, and static
verification through the Go module `github.com/paulmach/orb`; `make build` and
`make verify` provide stable aliases for build-through-test and full
verification. The gate also verifies the generated Mapbox Vector Tile source
and fixture set remain present.

The current focus is:

Priority:

- Preserve the small core geometry type model
- Keep geo and planar behavior separated by package
- Maintain test coverage for geometry equality, bounds, encoding, and algorithms
- Keep vet clean for parser, encoder, and geometry helper changes
- Keep package READMEs aligned with actual APIs
- Keep Go module metadata and dependency checksums current
- Keep degenerate rings and malformed geometry inputs panic-resistant
- Keep empty line strings safe in core helper methods
- Keep nil geometries in collections safe for aggregate helpers
- Keep empty bounds and empty union arguments safe as identity values in
  aggregate helpers
- Keep zero-area bounds valid and distinct from malformed negative bounds
- Keep empty polygons inside multipolygons safe in simplification helpers
- Keep empty rings and child polygons safe in smart clipping helpers
- Keep leading empty polygons safe in multipolygon bound aggregation
- Keep empty rings and polygons safe in planar containment helpers
- Keep empty interval resampling safe before distance precomputation
- Keep descendant tile operations inside the `maptile.MaxZoom` coordinate ceiling
- Keep above-ceiling tile-cover sets stable instead of traversing nonexistent siblings
- Keep non-finite interval distances out of resampling calculations and
  caller-provided distance callbacks
- Keep nonfinite and integer-overflowing derived point counts out of resampling
  allocation
- Keep negative derived point counts out of resampling conversion and allocation
- Keep non-finite callback distances and cumulative totals out of both resampling entry points
- Keep negative callback segment distances out of cumulative resampling geometry
- Keep a zero callback total out of interpolation while preserving mixed
  zero-length and positive callback segments
- Keep resampling callback, coordinate, progress, and output-allocation
  boundaries finite and explicitly bounded
- Keep polygon distance indices aligned with the matching immediate ring
- Keep the race detector in the canonical verification gate
- Keep fixed Go 1.20.14 and patched Go 1.25.11 validation in pinned, read-only,
  credential-free hosted Linux CI
- Keep the Go compatibility minimum, modern validation lane, module path,
  toolchain-selection boundary, and generated-code expectations explicit

Next priorities:

- Add regression fixtures for edge cases in clipping and simplification
- Add more edge-case fixtures for empty and degenerate core geometries
- Add resampling fixtures for empty, single-point, and zero-length lines
- Add aggregate-bound fixtures for leading empty polygons and geometry groups
- Add more planar containment fixtures for malformed ring and polygon inputs
- Keep encoding packages explicit about coordinate order and projection context
- Review benchmark coverage for geometry-heavy operations

Contribution rules:

- One PR = one focused type, algorithm, encoding, or documentation change.
- Add tests for geometric edge cases and numeric tolerances.
- Avoid changing exported behavior without migration notes.
- Keep new packages composable with the base `orb.Geometry` interface.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Geometry libraries are often used in data pipelines. Contributions should avoid
panic-prone parsing, unbounded memory growth on malformed inputs, and ambiguous
coordinate handling.

## What We Will Not Merge (For Now)

- Breaking core type changes without a migration plan
- Algorithm rewrites without fixtures and benchmarks
- Hidden global state in geometry operations
- Encoding behavior that silently changes coordinate semantics

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
