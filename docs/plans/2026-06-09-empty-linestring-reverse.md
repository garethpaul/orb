# Empty LineString Reverse Plan

status: completed

## Context

`LineString.Reverse` used an index calculation that panicked for empty line
strings. Geometry helpers should tolerate empty inputs because callers often
process malformed or degenerate data in pipelines.

## Objectives

- Make `LineString.Reverse` a no-op for empty and single-point line strings.
- Add a regression test for empty line-string reversal.
- Extend the static baseline and docs for the empty-input behavior.

## Verification

- `go test .`
- `make check`
- `go test ./...`
- `go vet ./...`
- `python3 scripts/check-baseline.py`
- `git diff --check`
