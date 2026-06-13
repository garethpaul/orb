# Location-Independent Make Gates

status: planned

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
  boundary, race coverage, and dependency-free static checker.
- Statically reject caller-relative or caller-overridable gate execution.
- Record completed verification from both repository-root and external working
  directories on the declared Go validation lanes.

## Scope Boundaries

- Do not change geometry behavior, public APIs, module identity, dependencies,
  generated protobuf sources, fixtures, or workflow coverage.
- Do not alter the Go 1.20.14 compatibility lane or patched Go 1.25.11 lane.
- Do not weaken the sparse baseline, race detector, vet, tests, or hosted gate.

## Implementation Units

1. Root every Make recipe at the Makefile's repository while preserving the
   current aliases and command semantics.
2. Extend `scripts/check-baseline.py` to require the rooted recipes, this plan,
   completed evidence, and the unchanged sparse tracked-file boundary.
3. Document the external invocation contract in `README.md` and `CHANGES.md`.

## Verification Plan

- Run all standard aliases on Go 1.20.14 and Go 1.25.11 from the repository
  root and through the absolute Makefile path from `/tmp`.
- Confirm a caller-supplied repository-root variable cannot redirect commands.
- Parse workflow YAML, compile the Python checker outside the repository, and
  run isolated hostile mutations over the rooted Make and evidence contracts.
- Audit intended paths, whitespace, generated artifacts, and secret-like data.
