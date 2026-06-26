# MVT Invalid Geometry Marshal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make public MVT marshaling reject nil, empty, and too-short geometry components with errors instead of panicking or emitting invalid commands.

**Architecture:** Keep validation at the private MVT encoder boundary used by `Marshal`. Validate each concrete geometry shape before indexing points or writing commands, then let the existing layer/feature error wrapping provide public context.

**Tech Stack:** Go 1.20, Orb geometry types, Mapbox Vector Tile protobuf encoding, table-driven Go tests, Python static contracts, GNU Make, GitHub Actions.

---

## Status: Completed

Completed on 2026-06-25. The implementation was reviewed at commit
`88968004a1c36229d8a86359b75328996080c6de`. Hosted Check runs `28212959729`
and `28212963171` passed on Go 1.20.14, Go 1.25.3, and Go 1.25.11, and CodeQL
run `28212962853` passed for actions, Go, and Python. The local Codex review
helper selected `codex review --base origin/master` but could not authenticate
to the OpenAI API (HTTP 401); exact-head manual review found no actionable
findings.

### Task 1: Reproduce public failures

- Add table-driven `Marshal` cases for every nil, empty, or too-short encoded component.
- Recover panics only to report them as test failures.
- Require a non-nil contextual error for every case.

### Task 2: Validate before encoding

- Reject empty multipoints and collections.
- Require at least two points per line and three points per ring.
- Enforce the same minimums for multiline, polygon, and multipolygon children.
- Preserve well-formed encoding behavior and existing error wrapping.

### Task 3: Preserve the boundary

- Add static contracts for source guards, tests, plans, and public guidance.
- Run hostile mutations that remove top-level or nested checks.
- Record the complete maintenance cycle in `CHANGES.md`.

### Task 4: Validate and publish

- Run focused and full gates on Go 1.20.14 and Go 1.25.11.
- Review the exact branch against `origin/master`.
- Open a focused PR and merge only after hosted checks pass.

## Verification Evidence

- Focused RED on Go 1.20.14 reproduced missing errors, index panics, and
  nonconformant one-point line and two-point ring acceptance.
- Full `make check` and `go mod verify` passed in pinned Go 1.20.14 and Go
  1.25.11 containers, including all package tests, race tests, vet, workflow and
  static contracts, and Make-root isolation.
- Twelve isolated hostile mutations were rejected across the encoder call, nil
  guard, top-level collections, nested children, and line/ring minimums.
- Both hosted test matrices and every CodeQL analysis lane passed.
