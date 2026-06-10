# MultiPolygon Empty Bound Plan

status: completed

## Context

`MultiLineString.Bound` already has direct coverage for a leading empty child
line string. `MultiPolygon.Bound` relies on the same empty-bound identity
contract through `Bound.Union`, but lacked a focused regression for leading
empty polygons.

## Objectives

- Add direct Go coverage for `MultiPolygon.Bound` with leading empty polygons.
- Preserve aggregate bounds for later non-empty polygons.
- Extend static checks and docs so leading empty polygons stay covered.

## Verification

- `go test .`
- `go test ./...`
- `go vet ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
