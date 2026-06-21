# Safe Make Root

## Problem

Whitespace-splitting Make functions and caller-controlled `MAKEFILE_LIST`
values could redirect Go verification outside the checkout.

## Change

- Resolve the raw Makefile path with POSIX-compatible system tooling.
- Reject non-file origins for GNU Make's automatic `MAKEFILE_LIST` value.
- Add dependency-free regressions for every public target, spaces, a literal
  apostrophe, command-line and environment `REPO_ROOT`, and command-line and
  environment `MAKEFILE_LIST` injection.

## Validation

- Run Go tests, race detection, vet, static checks, and workflow contracts.
- Run root-policy tests without credentials or network services.
- Confirm all three supported Go lanes and CodeQL pass at the exact pull-request
  head.
