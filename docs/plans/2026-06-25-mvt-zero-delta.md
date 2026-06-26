# MVT Degenerate Segment Marshal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make public MVT marshaling reject encoded zero-length line segments and invalid ring command sequences.

**Architecture:** Extend the private pre-encoding geometry validator with helpers that compare the `int32` coordinates written by the command encoder. Reuse the helpers for top-level and nested line and ring types so public `Marshal` continues returning layer/feature contextual errors.

**Tech Stack:** Go 1.20, Orb geometry types, Mapbox Vector Tile 2.1 command encoding, table-driven Go tests, Python static contracts, GNU Make, GitHub Actions.

---

## Status: Completed

Completed on 2026-06-25. The implementation was reviewed at commit
`ac71104f812d261b07b63864641b8c6813883b68`. Hosted Check runs `28213260959`
and `28213262667` passed on Go 1.20.14, Go 1.25.3, and Go 1.25.11, and CodeQL
run `28213261684` passed for actions, Go, and Python. The local Codex review
helper selected `codex review --base origin/master` but could not authenticate
to the OpenAI API (HTTP 401); exact-head manual review found no actionable
findings.

### Task 1: Reproduce public failures

- Add table-driven `Marshal` cases for exact and quantized line collapse.
- Cover nested multiline, polygon, and multipolygon components.
- Cover explicitly closed rings with too few encoded vertices.
- Assert redundant line and ring vertices produce canonical command streams.

### Task 2: Validate encoded segments

- Compare coordinates after the encoder's `int32` conversion.
- Remove adjacent encoded-equal line and ring vertices.
- Require at least three encoded ring vertices after removing an explicit close.
- Reject lines and rings that collapse below their command-count minimums.

### Task 3: Preserve the boundary

- Add static contracts for source guards, tests, plans, and public guidance.
- Run isolated hostile mutations across top-level and nested validation paths.
- Record the complete maintenance cycle in `CHANGES.md`.

### Task 4: Validate and publish

- Run focused and full gates on Go 1.20.14 and Go 1.25.11.
- Review the exact branch against `origin/master`.
- Open a focused PR and merge only after hosted checks pass.

## Verification Evidence

- Focused RED on Go 1.20.14 accepted all seven geometries that collapsed below
  valid line or ring command counts.
- Focused and full `encoding/mvt` tests passed on Go 1.20.14 and Go 1.25.11,
  including canonical command assertions for normalized line and ring vertices.
- Full `make check` and `go mod verify` passed in pinned Go 1.20.14 and Go
  1.25.11 containers, including all packages, race tests, vet, workflow and
  static contracts, and Make-root isolation.
- Twelve isolated hostile mutations were rejected across integer-coordinate
  comparison, lazy normalization, collapse minimums, ring closure, and every
  top-level or nested encoder path.
