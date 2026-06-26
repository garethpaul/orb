---
title: Maptile Fraction Boundary
date: 2026-06-25
type: implementation-plan
status: completed
---

# Maptile Fraction Boundary

## Problem

`maptile.Fraction` returned infinities or NaNs at zoom 1024 and above. Line and
polygon tile covers bypassed `maptile.At`, allowing unrepresentable zooms to
enter traversal that could require enormous work or fail to progress.

## Requirements

- Preserve finite fraction scales through zoom 1023.
- Saturate larger fraction exponents at the largest finite scale.
- Saturate overflowing finite longitude products at `math.MaxFloat64`.
- Return empty tile covers above `maptile.MaxZoom` before wrapper iteration.
- Preserve public APIs and Go 1.20 compatibility.

## Verification

- RED: Go 1.20.14 reproduced non-finite `TestFraction` results at zoom 1024 and
  `math.MaxUint32`.
- Focused `TestFraction` and `TestExcessiveZoomLineAndPolygonCovers` pass after
  the finite-scale and fail-closed traversal guards.
- Full `make check` and `go mod verify` pass on Go 1.20.14 and Go 1.25.11.
- Seven meaningful hostile mutations removing the fraction guard, lowering the
  finite boundary, removing longitude saturation, or deleting traversal and
  wrapper guards are rejected.
- Local implementation verification is complete; review and hosted validation
  remain landing steps before merge.
