# Simplify Empty Multipolygon Plan

status: completed

## Context

`simplify.multiPolygon` simplified each child polygon and then inspected
`p[0]` to decide whether to keep it. A malformed multipolygon containing an
empty polygon could panic before the helper had a chance to skip the empty
geometry.

## Objectives

- Skip simplified child polygons when the polygon slice is empty.
- Preserve the existing behavior that drops polygons whose outer ring has two
  or fewer points after simplification.
- Add a Go regression test for an empty polygon inside a multipolygon.
- Extend static checks and docs so the panic-resistant behavior remains covered.

## Verification

- `go test ./simplify`
- `go test ./...`
- `go vet ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
