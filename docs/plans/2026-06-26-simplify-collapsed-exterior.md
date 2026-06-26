# Simplify Collapsed Exterior Ring Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make direct polygon simplification drop a polygon whose exterior ring collapses below the minimum valid size.

**Architecture:** Keep the fix in the shared `polygon` helper used by Douglas-Peucker, radial, and Visvalingam simplifiers. Reject only a collapsed exterior; retain the existing compaction behavior for valid exteriors and interior rings.

**Tech Stack:** Go 1.20, Orb geometry types, table-driven Go tests, Python static contracts, GNU Make, GitHub Actions.

---

## Status: Completed

Completed locally on 2026-06-26. The exact branch still requires hosted test
matrices and Codex review before merge.

### Task 1: Add the failing public regression

**Files:**
- Modify: `simplify/helpers_test.go`

1. Add `TestPolygonSkipsCollapsedExteriorRing` with a closed square.
2. Simplify it with `DouglasPeucker(100)`.
3. Assert the public `Polygon` result is empty.
4. Add `TestPolygonDoesNotPromoteInteriorRing` with a collapsed exterior and
   surviving inner ring.
5. Run the focused tests on Go 1.20.14 and confirm RED returns invalid polygon data.

### Task 2: Fix shared polygon validity

**Files:**
- Modify: `simplify/helpers.go`

1. Return an empty polygon when the simplified exterior has two or fewer points.
2. Keep skipping collapsed interior rings.
3. Run the focused test and the full `simplify` package on Go 1.20.14.

### Task 3: Preserve the contract

**Files:**
- Modify: `scripts/check-baseline.py`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `AGENTS.md`
- Modify: `CHANGES.md`

1. Require the exterior guard, regression name, plans, and public guidance.
2. Run hostile mutations that remove or weaken the guard and regression evidence.
3. Record the cycle, validation, review, and merge evidence.

### Task 4: Validate and publish

1. Run focused and full gates on Go 1.20.14 and Go 1.25.11.
2. Run `go mod verify`, formatting, diff, and exact-head manual review.
3. Open a focused PR, run `codex review --base origin/master`, and merge only after hosted checks pass.

## Verification Evidence

- RED: Go 1.20.14 returned a two-point exterior from the public `Polygon` helper.
- Focused and full `simplify` package tests passed on Go 1.20.14 and Go 1.25.11.
- The static documentation contract failed before synchronized guidance existed.
- `GOTOOLCHAIN=go1.20.14 make check` and `GOTOOLCHAIN=go1.25.11 make check`
  passed with package, Linux/386 WKB, race, vet, workflow, static, and Make-root checks.
- `GOTOOLCHAIN=go1.20.14 go mod verify` and
  `GOTOOLCHAIN=go1.25.11 go mod verify` passed.
- Three hostile mutations were rejected for the exterior guard,
  interior-ownership regression, and completed plan evidence.
- Direct correctness, quality, and security review found no actionable issue.
