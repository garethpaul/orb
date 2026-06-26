# WKB Architecture-Safe Count Loops Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Prevent high-bit WKB element counts from being accepted as empty geometries on 32-bit Go builds.

**Architecture:** Keep decoded counts and loop indices as `uint32`, matching the WKB wire field. Preserve existing capped preallocation and streaming reads; add a Linux/386 test gate to exercise the architecture-specific failure mode.

**Tech Stack:** Go 1.20+, standard `encoding/binary`, GNU Make, Python static contracts.

---

### Task 1: Add the failing 386 regression

**Files:**
- Create: `encoding/wkb/count_test.go`
- Modify: `Makefile`
- Modify: `scripts/check-baseline.py`

**Step 1:** Add table-driven WKB headers with aggregate types and count `0x80000000`.

**Step 2:** Assert `Unmarshal` returns `ErrNotWKB` for each truncated payload.

**Step 3:** Add a Linux-only `GOARCH=386 go test ./encoding/wkb` command to `make test`.

**Step 4:** Run the 386 package test and confirm it fails by accepting an empty geometry.

### Task 2: Preserve uint32 count semantics

**Files:**
- Modify: `encoding/wkb/point.go`
- Modify: `encoding/wkb/line_string.go`
- Modify: `encoding/wkb/polygon.go`
- Modify: `encoding/wkb/collection.go`

**Step 1:** Replace all six `int(num)` loop bounds with `uint32` loop indices.

**Step 2:** Run native and Linux/386 WKB tests and confirm both pass.

**Step 3:** Run `gofmt` on the new test.

### Task 3: Validate and document

**Files:**
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`

**Step 1:** Document architecture-safe untrusted count handling.

**Step 2:** Run `make check` with Go 1.20.14 and Go 1.25.11.

**Step 3:** Mutate one loop back to `int(num)` and confirm static verification fails.

**Step 4:** Commit, open a PR, run Codex review, require hosted checks, and merge.

## Verification Evidence

- RED: Go 1.20.14/386 accepted a multipoint count of `0x80000000` as an empty
  geometry with no error.
- Native and Linux/386 WKB package tests pass after all six loops retain
  `uint32` indices.
- Full `make check` and `go mod verify` pass on Go 1.20.14 and Go 1.25.11.
- A hostile `int(num)` loop mutation is rejected by the static baseline.
