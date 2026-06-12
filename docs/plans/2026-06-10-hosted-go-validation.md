# Hosted Go Validation

status: completed

## Context

The geometry library has broad unit coverage and local vet checks, but no
hosted validation. Concurrent callers also depend on helpers remaining free of
shared-state races, while the canonical gate does not run Go's race detector.

## Priorities

1. Add the race detector to the canonical local and hosted gate.
2. Test the declared Go 1.20 baseline and the currently exercised Go 1.25 line.
3. Pin workflow actions, Go patches, permissions, runner, and timeout.
4. Disable automatic Go toolchain switching in the version matrix.
5. Enforce the hosted workflow contract from the static checker.

## Implementation Units

Files:

- `.github/workflows/check.yml`
- `Makefile`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`

Add `go test -race ./...` as a dedicated Make target included by `make check`.
Run the full gate on fixed Go 1.20.14 and Go 1.25.3 hosted Linux jobs using
commit-pinned Node.js 24-compatible checkout and Go setup actions with
`GOTOOLCHAIN=local`.

## Verification

- `make lint`
- `make test`
- `make race`
- `make build`
- `make check`
- Go 1.20.14 container: race tests and vet
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for both Go versions

## Boundaries

- Do not change geometry behavior or public APIs.
- Do not upgrade the module's declared minimum Go version.
- Do not update dependencies in this pass.
