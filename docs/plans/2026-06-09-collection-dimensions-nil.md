# Collection Dimensions Nil Guard

status: completed

## Context

`Collection.Bound()` skipped nil geometries, but `Collection.Dimensions()`
called `Dimensions()` on every collection entry. A collection with a nil
geometry could panic in dimension checks even though the bound path already
tolerated the same malformed input.

## Objectives

- Skip nil geometries while computing collection dimensions.
- Preserve the existing `-1` dimension result for empty or all-nil
  collections.
- Add Go tests for nil-only, nil-leading, and nil-between collection entries.
- Extend the static baseline and docs so nil geometry collections stay covered.

## Verification

- `go test .`
- `go test ./...`
- `go vet ./...`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
