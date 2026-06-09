# Planar Empty Containment Plan

status: completed

## Context

`planar.RingContains` indexed the first and last ring points before checking
whether the ring had any coordinates. `planar.PolygonContains` also indexed the
outer ring directly. Malformed empty rings or polygons could therefore panic in
caller geometry pipelines.

## Objectives

- Return false for empty rings in `RingContains`.
- Return false for empty polygons in `PolygonContains`.
- Keep `MultiPolygonContains` safe when a multipolygon includes empty child
  polygons.
- Add regression tests and static baseline coverage for these malformed inputs.
- Document the containment guardrail in README, SECURITY, VISION, and CHANGES.

## Verification

- `go test ./planar`
- `go test ./...`
- `go vet ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
