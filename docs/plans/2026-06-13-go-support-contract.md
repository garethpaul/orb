# Go Support Contract

status: completed

## Context

The repository declares `go 1.20` and tests fixed Go 1.20.14 and 1.25.3 lanes,
but contributor guidance does not state which version is the compatibility
minimum, what the modern lane proves, whether automatic toolchain selection is
allowed, or which module and generated-code surfaces must remain stable.

## Priorities

1. Define the supported Go version and toolchain boundary without changing it.
2. Make module-path, dependency-integrity, and generated-code expectations
   explicit for contributors and consumers.
3. Enforce the documentation and completed evidence in the existing baseline.

## Requirements

- R1. Identify Go 1.20 as the declared language compatibility minimum and Go
  1.20.14 as the fixed final-patch compatibility lane.
- R2. Identify Go 1.25.3 as a fixed modern validation lane, not a raised minimum
  or promise that every future Go release is supported automatically.
- R3. Preserve `GOTOOLCHAIN=local` in hosted validation and prohibit a checked-in
  `toolchain` directive unless a reviewed support-policy change requires one.
- R4. Preserve module path `github.com/paulmach/orb`; treat a path change as a
  breaking import migration requiring explicit authorization and release notes.
- R5. Require `go mod verify`, synchronized `go.mod`/`go.sum`, and review of
  direct plus transitive changes before dependency updates.
- R6. Keep generated Mapbox Vector Tile protobuf source, schema, and fixtures in
  sync without hand-editing generated output.
- R7. Require both fixed toolchains to pass the canonical tests, race detector,
  vet, build, and sparse baseline before support-policy changes are accepted.
- R8. Enforce the support contract through the existing dependency-free checker.

## Scope Boundaries

- Do not change Go versions, module metadata, dependencies, generated code, or
  geometry behavior in this unit.
- Do not claim support for untested Go releases or platforms.
- Do not reformat unrelated Go files or generated output.

## Verification Plan

- `GOTOOLCHAIN=go1.20.14 make check`
- `GOTOOLCHAIN=go1.25.3 make check`
- `GOTOOLCHAIN=go1.20.14 go mod verify`
- `GOTOOLCHAIN=go1.25.3 go mod verify`
- parse workflow YAML
- run the checker from an external working directory
- run focused hostile mutations against the support contract
- `git diff --check`
- scan the intended diff for secrets and generated artifacts

## Work Completed

Documented the declared minimum, fixed compatibility and modern validation
lanes, local-toolchain boundary, module-path stability, dependency integrity,
and generated protobuf expectations without changing those surfaces.

## Verification Completed

- `GOTOOLCHAIN=go1.20.14 make check` and `GOTOOLCHAIN=go1.25.3 make check`
  passed.
- `GOTOOLCHAIN=go1.20.14 go mod verify` and
  `GOTOOLCHAIN=go1.25.3 go mod verify` passed.
- The checker passed from an external working directory, and workflow YAML
  parsed successfully.
- Ten focused hostile mutations rejected weakened support-contract and plan
  evidence; `hostile mutations rejected` was verified explicitly.
- `git diff --check` and the intended-diff secret and generated-artifact scan
  passed.
