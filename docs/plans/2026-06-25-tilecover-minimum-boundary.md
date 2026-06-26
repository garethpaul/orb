---
title: Tile-Cover Minimum Boundary
date: 2026-06-25
type: implementation-plan
status: in-progress
---

# Tile-Cover Minimum Boundary

## Problem

`MergeUp` and `MergeUpPartial` determine the uniform input zoom and merge toward
a numerically lower minimum. When the requested minimum exceeded the input zoom,
their equality-only boundary checks missed the no-op case, the merge loops ran
zero times, and both functions returned a newly allocated empty set.

## Requirements

- Preserve same-zoom input sets when the requested minimum equals or exceeds the
  input zoom.
- Preserve existing downward merge behavior when the minimum is lower.
- Keep above-`MaxZoom` preservation and public signatures unchanged.
- Preserve unsupported mixed-zoom sets before sibling indexing can panic.
- Cover complete and partial variants with a focused regression.
- Keep the correction compatible with Go 1.20.

## Verification

- RED: Go 1.20.14 reproduced empty output from both variants for a zoom-2 tile
  and minimum zoom 3.
- Four independent investigations agreed that `min >= max` is the narrowest
  contract-compatible minimum correction. Review then reproduced a mixed-zoom
  panic, so both variants now share order-independent zoom validation and return
  unsupported sets unchanged.
- Focused regressions pass on Go 1.20.14.
- Full `make check` passes on Go 1.20.14 and Go 1.25.11, including tests, race,
  vet, workflow contracts, the static baseline, and Make authority tests.
- Four hostile mutations reverting either minimum guard, excessive-zoom
  rejection, or mixed-zoom rejection are rejected by focused regressions.
- Independent implementation review, exact-head Codex review, and hosted CI are
  pending before merge.
