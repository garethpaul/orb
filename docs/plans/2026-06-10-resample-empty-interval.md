# Empty Interval Resampling

status: completed

## Context

`resample.ToInterval` computes segment distances before running the shared line
edge-case handler. For an empty line string this creates a slice with length
`-1` and panics, unlike `Resample`, which handles empty input first.

## Objectives

- Return nil and non-nil empty line strings unchanged for positive intervals.
- Guard empty and single-point inputs before distance precomputation.
- Prove caller-provided distance functions are not invoked for empty input.
- Extend the active baseline and project guidance for empty interval resampling.

## Verification

- `go test ./...`
- `go test -race ./...`
- `go vet ./...`
- `make check`
- `git diff --check`
