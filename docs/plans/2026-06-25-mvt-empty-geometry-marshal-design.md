# MVT Invalid Geometry Marshal Design

## Status: Accepted

## Problem

`mvt.Marshal` forwards feature geometries to `encodeGeometry`, which indexes the
first point of line strings and rings without validating their length. Empty
components can therefore panic the caller. Empty multipoints and multipolygons,
one-point lines, and rings with fewer than three points can also emit missing or
zero-count commands that violate the MVT 2.1 geometry command requirements.

The normative command-count requirements are documented in the
[Mapbox Vector Tile 2.1 specification](https://github.com/mapbox/vector-tile-spec/tree/master/2.1):
point `MoveTo` counts must be positive, line `LineTo` counts must be positive,
and polygon ring `LineTo` counts must be greater than one.

## Constraints

- Preserve public APIs and well-formed MVT output.
- Return errors through the existing `Marshal` error path instead of panicking.
- Do not silently drop features or malformed child components.
- Keep errors contextualized with the existing layer and feature indices.
- Preserve Go 1.20 compatibility.

## Options Considered

1. **Reject nil, empty, and too-short encoded components with errors.**
   Recommended because it uses the existing public error channel, enforces the
   command-count requirements, and avoids silently changing feature data.
2. Skip empty features or child components. Rejected because `Marshal` should
   not mutate caller intent or desynchronize properties and feature counts.
3. Emit zero-count or partial geometry commands. Rejected because malformed MVT
   output defers failure to downstream decoders and does not prevent panics.

## Decision

Validate every collection-like geometry before indexing or emitting commands.
Return a stable error for nil geometry, empty multipoints or collections, lines
with fewer than two points, and rings with fewer than three points at every
nested level. Exercise the public `Marshal` path and assert both error return
and panic absence.

## Validation

- Observe current `Marshal` behavior fail the focused table through panics or
  missing errors.
- Pass focused tests on Go 1.20.14 and Go 1.25.11.
- Run both full pinned Make gates, mutation checks, hosted matrices, and CodeQL.
