# Collection Bound Fixtures

Status: Completed

## Context

The roadmap requested aggregate-bound fixtures for leading empty polygons and
geometry groups. `MultiPolygon.Bound` already covered a leading empty polygon,
and `Collection.Bound` already skipped nil children, but the public collection
helper lacked direct coverage for a leading empty geometry and nested geometry groups.

## Decision

- Add a regression where a leading empty line string precedes a non-empty
  polygon and must remain an aggregate identity.
- Add a nested collection regression combining empty children, a multipolygon
  with a leading empty polygon, a nil child, and a point.
- Preserve the complete union of nested non-empty bounds.
- No production source change was required because the existing empty-bound
  identity behavior already satisfies both public contracts.

## Verification

- Focused root-package tests passed with Go 1.20.14 and Go 1.25.11.
- `GOTOOLCHAIN=go1.20.14 make check` and
  `GOTOOLCHAIN=go1.25.11 make check` passed in pinned containers, including all
  packages, Linux/386 WKB tests, race tests, vet, workflow/static contracts,
  and Make-root isolation.
- `go mod verify` passed in both pinned lanes.
- Five isolated hostile mutations were rejected for both fixture names, README
  guidance, roadmap completion, and plan status.
- `git diff --check` passed.

## Residual Risk

These deterministic planar fixtures do not exercise every geometry nesting
depth or non-finite coordinate. Existing type-specific bound contracts remain
responsible for validating each child geometry's own result.
