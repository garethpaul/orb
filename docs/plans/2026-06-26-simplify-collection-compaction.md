# Simplify Collection Compaction

Status: Completed

## Context

The public collection simplifier replaced collapsed child geometries with nil
but preserved their slice positions. A collection containing nil, a polygon
collapsed by Douglas-Peucker simplification, and a point returned
`[<nil> <nil> [5 6]]`. A collection whose children all collapsed remained a
non-empty collection of nil values, so the generic `Simplify` API could not
return nil for an empty result.

The upstream `paulmach/orb` helper currently retains the same behavior. This
fork intentionally strengthens the result contract rather than claiming an
upstream synchronization.

## Decision

- Simplify each collection child recursively.
- Skip nil simplification results and compact surviving geometries in place.
- Preserve survivor order and nested collection boundaries.
- Return an empty collection when no child survives, allowing generic
  `Simplify` to return nil for a fully collapsed collection.

## Verification

- RED on Go 1.20.14: the mixed collection returned
  `[<nil> <nil> [5 6]]`, and the fully collapsed collection returned
  `[<nil> <nil>]`.
- Focused package tests pass on Go 1.20.14 and Go 1.25.11.
- Full `make check` and `go mod verify` pass on Go 1.20.14 and Go 1.25.11,
  including all packages, Linux/386 WKB tests, race tests, vet,
  workflow/static contracts, and Make-root isolation.
- Ten isolated hostile mutations were rejected across the compaction source,
  both regressions, plan status, and all four guidance files.
- `git diff --check` passed.

## Residual Risk

The collection slice is still reused as documented by the simplifier APIs.
Callers that need the original input must clone it before simplification.
