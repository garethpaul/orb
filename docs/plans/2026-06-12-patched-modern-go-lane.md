# Patched modern Go validation lane

status: completed

## Context

The module intentionally declares Go 1.20 compatibility, but the modern hosted
lane was pinned to Go 1.25.3 after later patch releases were available. A local
`govulncheck` review found 0 reachable vulnerabilities in orb code; findings in
the older standard library reinforce keeping the modern validation lane on a
patched toolchain without unnecessarily raising the public module minimum.

## Decision

1. Preserve the Go 1.20 module declaration and verify its final patch release,
   Go 1.20.14.
2. Move the modern hosted lane to Go 1.25.11 with `GOTOOLCHAIN=local` so both
   compatibility claims are explicit and reproducible.
3. Keep third-party actions pinned to full commits and set
   `persist-credentials: false` on checkout.
4. Enforce the exact toolchain matrix, action allowlist, read-only permissions,
   and credential handling in `scripts/check-baseline.py`.

## Verification

- `GOTOOLCHAIN=go1.20.14 make check`
- `GOTOOLCHAIN=go1.25.11 make check`
- `GOTOOLCHAIN=go1.25.11 go run golang.org/x/vuln/cmd/govulncheck@latest ./...`
- hostile workflow and documentation mutation checks
- `git diff --check`

The scan recorded 0 reachable vulnerabilities. Dependency-only or standard
library advisories remain reasons to keep validation toolchains patched, not to
break the module's documented minimum without a separate compatibility plan.
