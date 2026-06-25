---
title: Maptile Descendant Boundary
date: 2026-06-25
type: implementation-plan
status: completed
---

# Maptile Descendant Boundary

## Problem

`maptile.MaxZoom` is the highest level whose complete tile coordinate range is
representable in `uint32`. `Tile.Children` still shifted coordinates beyond
that ceiling, and `Tile.Range` preserved wrapped payload coordinates for higher
target zooms.

## Requirements

- Treat tiles at `MaxZoom` and above as having no children.
- Preserve four-child behavior for every valid tile below `MaxZoom`.
- Preserve valid ranges through `MaxZoom`.
- Return invalid zero-coordinate endpoints at the requested zoom for targets
  above `MaxZoom`.
- Preserve above-ceiling tile-cover sets unchanged instead of indexing a
  nonexistent sibling list.
- Keep the public API and Go 1.20 compatibility unchanged.

## Verification

- RED: Go 1.20.14 focused tests observed wrapped children and noncanonical
  above-ceiling ranges before the implementation.
- A first attempt also treated every invalid tile as a leaf. Full tests exposed
  that tile-cover merging traverses invalid intermediate tiles, so that broader
  behavior was reverted while retaining the `MaxZoom` ceiling.
- Focused `go test ./maptile ./maptile/tilecover` passed on Go 1.20.14.
- Full offline `make check` passed on Go 1.20.14 and Go 1.25.11, including all
  package tests, race tests, vet, workflow contracts, the static baseline, and
  Make authority tests.
- Exact-head review reproduced a panic when `MergeUp` received a tile above
  `MaxZoom`; both complete and partial tile-cover merging now return that set
  unchanged, with a focused regression test.
- The complete offline `make check` matrix passed again after that review fix
  on Go 1.20.14 and Go 1.25.11.
- Six hostile mutations were rejected: missing and strict child guards,
  missing range guard, noncanonical invalid range payload, and removal of
  either complete or partial merge guard.
- Exact-head Codex review at `0ecd00c` reported no actionable findings.
- Both hosted test matrices passed on Go 1.20.14, Go 1.25.3, and Go 1.25.11;
  the actions, Go, and Python CodeQL analyses also passed.
