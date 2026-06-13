# Patched Modern Go Lane

status: pending

## Context

The stacked Go support-contract branch describes Go 1.25.3 as its fixed modern
validation lane. Go 1.25.11 was released on June 2, 2026 with security fixes,
and the earlier remediation branch already selected that patched release. The
active workflow and current support documentation should not regress to the
older toolchain.

## Requirements

- Preserve Go 1.20 as the declared compatibility minimum and Go 1.20.14 as its
  fixed final-patch validation lane.
- Move the active modern workflow and support contract from Go 1.25.3 to Go
  1.25.11 with `GOTOOLCHAIN=local`.
- Keep historical plans and hosted evidence unchanged where they truthfully
  record validation that previously ran on Go 1.25.3.
- Run tests, race detection, vet, module verification, and vulnerability
  analysis on the patched modern lane.
- Add mutation-sensitive static and completed-plan contracts.

## Scope Boundaries

- Do not raise the `go 1.20` module directive or add a `toolchain` directive.
- Do not change geometry behavior, dependencies, protobuf files, or fixtures.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and validation.
