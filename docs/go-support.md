# Go Support Contract

Review date: 2026-06-13

## Compatibility Minimum

The module declares `go 1.20`. Go 1.20 is therefore the language and module
compatibility minimum for this branch, and the fixed Go 1.20.14 lane exercises
the final patch release in that line. Changes must not introduce syntax,
standard-library APIs, build constraints, or module behavior unavailable to
that lane without an explicit support-policy change.

The fixed Go 1.25.3 lane is modern-toolchain validation. It catches newer
compiler, vet, race-detector, and module behavior, but it does not raise the
declared minimum or promise automatic support for every newer Go release.

Hosted jobs set `GOTOOLCHAIN=local`. The repository intentionally has no
`toolchain` directive, so local and hosted validation do not silently download
or switch to a different Go toolchain. Adding such a directive requires a
reviewed support-policy change.

## Module Boundary

The public module path is `github.com/paulmach/orb`. Changing it is a breaking
import migration and requires explicit authorization, migration notes, and an
appropriate release boundary. Package moves and exported API changes require
the same compatibility review even when `go test ./...` remains green.

Dependency changes must keep `go.mod` and `go.sum` synchronized, pass
`go mod verify`, and identify direct and transitive graph changes. Do not use an
automatic toolchain upgrade to make a dependency change pass on only one lane.

## Generated Code And Fixtures

Mapbox Vector Tile support includes the checked-in protobuf schema, generated
Go source, and binary fixtures. Regenerate these surfaces from the documented
schema and generator rather than hand-editing generated output, and review the
schema, generated diff, fixture impact, and module graph together.

## Required Validation

Support-policy, module, dependency, generated-code, and exported API changes
must pass the canonical tests, race detector, vet, build, module verification,
and sparse baseline on both fixed Go 1.20.14 and Go 1.25.3 toolchains. A newer
toolchain may be evaluated separately, but it does not replace either required
lane until the support contract and hosted matrix are deliberately updated.
