# Location-Independent Make Gates

status: completed

## Context

The canonical Make gates pass from the repository root, but invoking the
Makefile by absolute path from another working directory resolves both Go
module operations and `scripts/check-baseline.py` against the caller. Shared
automation should not need to change directories before running the same test,
race, vet, build, verify, and static contracts.

## Requirements

- Derive an override-protected repository root from the Makefile location.
- Run Go test, race, and vet operations against that explicit module root.
- Invoke the Python sparse checker by its rooted path.
- Preserve the existing alias graph, Go 1.20 module contract, local-toolchain
  boundary, race coverage, required-file baseline, and dependency-free static
  checker.
- Statically reject caller-relative or caller-overridable gate execution.
- Record completed verification from both repository-root and external working
  directories on the declared Go validation lanes.

## Scope Boundaries

- Do not change geometry behavior, public APIs, module identity, dependencies,
  generated protobuf sources, fixtures, or workflow coverage.
- Do not alter the Go 1.20.14 compatibility lane or patched Go 1.25.11 lane.
- Do not weaken the static baseline, race detector, vet, tests, or hosted gate.

## Implementation Units

1. Root every Make recipe at the Makefile's repository while preserving the
   current aliases and command semantics.
2. Extend `scripts/check-baseline.py` to require the rooted recipes, this plan,
   completed evidence, and the unchanged required-file baseline.
3. Document the external invocation contract in `README.md` and `CHANGES.md`.

## Verification Plan

- Run all standard aliases on Go 1.20.14 and Go 1.25.11 from the repository
  root and through the absolute Makefile path from `/tmp`.
- Confirm a caller-supplied repository-root variable cannot redirect commands.
- Parse workflow YAML, compile the Python checker outside the repository, and
  run isolated hostile mutations over the rooted Make and evidence contracts.
- Audit intended paths, whitespace, generated artifacts, and secret-like data.

## Work Completed

The Makefile now derives an override-protected absolute repository root from
its own location. Go test, race, and vet recipes change to that module root in
a subshell, while the static checker is invoked by its rooted path. Existing
aliases, commands, toolchain lanes, and the required-file baseline remain
unchanged.

## Verification Completed

- `make test`, `make race`, `make lint`, `make build`, `make static-check`,
  `make verify`, and `make check` passed with `GOTOOLCHAIN=go1.20.14` and
  `GOTOOLCHAIN=go1.25.11` from the repository root.
- Every alias passed on both toolchains from `/tmp` through the repository's
  absolute Makefile path.
- External `make check` passed on both toolchains with caller-supplied
  `REPO_ROOT=/tmp`, confirming command-line variables cannot redirect gates.
- `GOTOOLCHAIN=go1.20.14 go mod verify` and
  `GOTOOLCHAIN=go1.25.11 go mod verify` passed.
- `python3 -m py_compile scripts/check-baseline.py` passed with bytecode routed
  outside the repository, and the pinned workflow YAML parsed successfully.
- Twelve isolated hostile mutations were rejected across root derivation,
  override resistance, Go and checker recipes, plan evidence, and maintenance
  documentation.
