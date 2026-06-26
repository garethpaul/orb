# MVT Invalid Geometry Marshal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make public MVT marshaling reject nil, empty, and too-short geometry components with errors instead of panicking or emitting invalid commands.

**Architecture:** Keep validation at the private MVT encoder boundary used by `Marshal`. Validate each concrete geometry shape before indexing points or writing commands, then let the existing layer/feature error wrapping provide public context.

**Tech Stack:** Go 1.20, Orb geometry types, Mapbox Vector Tile protobuf encoding, table-driven Go tests, Python static contracts, GNU Make, GitHub Actions.

---

## Status: In Progress

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
