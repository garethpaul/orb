# Simplify Collapsed Exterior Ring Design

## Status: Accepted

## Problem

All simplifiers share `simplify.polygon`. When a high threshold reduces a
polygon exterior to two identical endpoints, direct `Polygon` calls retain that
invalid ring. `MultiPolygon` calls the same helper and then drops the polygon,
so the two public APIs disagree for the same geometry.

## Constraints

- Preserve valid polygon simplification and existing interior-ring filtering.
- Keep all simplifiers on the shared helper path.
- Do not invent replacement vertices after the algorithm removes them.
- Preserve Go 1.20 compatibility and in-place behavior for retained polygons.

## Options Considered

1. **Return an empty polygon when its simplified exterior has two or fewer points.**
   Recommended because it matches the existing `MultiPolygon` validity rule and
   avoids returning a geometry that cannot represent a polygon boundary.
2. Preserve the collapsed exterior for direct `Polygon` callers. Rejected
   because it perpetuates invalid output and inconsistent public behavior.
3. Force every simplifier to retain a minimum exterior shape. Rejected because
   synthesizing or retaining vertices changes each algorithm's reduction
   semantics and substantially widens the implementation.

## Decision

Make `polygon` return an empty slice immediately when ring zero simplifies to
two or fewer points. Continue skipping collapsed interior rings and leave valid
exteriors unchanged.

## Validation

- Add a public `Polygon` regression that fails on the current two-point output.
- Pass focused simplify tests on Go 1.20.14 and Go 1.25.11.
- Run full pinned `make check`, mutation checks, hosted matrices, and CodeQL.
