# Degenerate Ring Guards

status: completed

## Context

`Ring.Closed()` indexed the first and last point without checking length, and
`Ring.Orientation()` indexed the first point before handling empty or very short
rings. These helpers can be called from geometry pipelines that receive
malformed input.

## Objectives

- Preserve normal closed-ring and orientation behavior.
- Treat rings with fewer than four points as not closed.
- Treat rings with fewer than three points, or zero-area rings, as
  zero-orientation.
- Add Go tests and static baseline checks for degenerate rings.

## Verification

- `go test ./...`
- `go vet ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
