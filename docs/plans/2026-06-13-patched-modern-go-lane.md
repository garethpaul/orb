# Patched Modern Go Lane

status: completed

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

- Pinned the active hosted modern-toolchain lane to Go 1.25.11 while retaining
  Go 1.20.14 as the compatibility lane and `GOTOOLCHAIN=local` as the hosted
  toolchain-selection boundary.
- Updated current support, security, roadmap, release-note, and contributor
  guidance to distinguish the patched modern lane from the declared minimum.
- Extended the sparse baseline checker to enforce the active workflow and
  documentation contract plus this completed plan's mutation-sensitive
  evidence, without rewriting historical Go 1.25.3 records.

## Verification Completed

- `GOTOOLCHAIN=go1.20.14 make check`
- `GOTOOLCHAIN=go1.25.11 make check`
- `GOTOOLCHAIN=go1.20.14 go mod verify`
- `GOTOOLCHAIN=go1.25.11 go mod verify`
- `GOTOOLCHAIN=go1.25.11 go run golang.org/x/vuln/cmd/govulncheck@latest ./...`
  reported no vulnerabilities.
- Parsed the workflow YAML and compiled the Python baseline checker.
- Confirmed hostile mutations to the workflow, support contract, checker, and
  completed-plan evidence are rejected.
- `git diff --check`
- Reviewed the exact diff and scanned intended paths for secrets and generated
  artifacts; no source, dependency, protobuf, or fixture files changed.
