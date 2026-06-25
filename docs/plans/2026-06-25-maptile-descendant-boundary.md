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
- Four hostile mutations were rejected: missing and strict child guards,
  missing range guard, and noncanonical invalid range payload.
- Hosted checks and exact-head review remain required before merge.
