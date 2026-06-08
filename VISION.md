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

Current baseline: `make check` runs `go test ./...` through the Go module
`github.com/paulmach/orb` and verifies the generated Mapbox Vector Tile source
and fixture set remain present.

The current focus is:

Priority:

- Preserve the small core geometry type model
- Keep geo and planar behavior separated by package
- Maintain test coverage for geometry equality, bounds, encoding, and algorithms
- Keep package READMEs aligned with actual APIs
- Keep Go module metadata and dependency checksums current

Next priorities:

- Document supported Go versions and module expectations
- Add regression fixtures for edge cases in clipping and simplification
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
