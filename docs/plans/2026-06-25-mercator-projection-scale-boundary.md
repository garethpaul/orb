---
title: Mercator Projection Scale Boundary
date: 2026-06-25
type: implementation-plan
status: completed
---

# Mercator Projection Scale Boundary

## Problem

The shared Mercator helpers accepted arbitrary `uint32` levels, but
`math.Exp2` overflows at level 1024. Power-of-two MVT projection also shifted
`uint32` tile origins before conversion to `float64`, wrapping valid tile
coordinates once zoom plus extent bits exceeded 32.

## Requirements

- Preserve the requested Mercator scale through level 1023.
- Saturate larger levels at the largest finite power-of-two scale.
- Preserve MVT's intentional effective levels above `maptile.MaxZoom`.
- Scale power-of-two MVT tile origins without integer narrowing.
- Treat an explicit zero MVT extent as the default extent before projection.
- Keep public APIs and Go 1.20 compatibility unchanged.

## Verification

- RED: Go 1.20.14 reproduced infinite Mercator coordinates at levels 1024 and
  `math.MaxUint32`, plausible incorrect inverse coordinates, and wrapped
  power-of-two MVT origins at tile zooms 21 and 32.
- Focused `go test ./internal/mercator ./encoding/mvt` passed on Go 1.20.14 after
  introducing the shared level 1023 finite-scale boundary and `math.Ldexp`
  origin scaling.
- Full `make check` and `go mod verify` passed on Go 1.20.14 and Go 1.25.11.
- Seven meaningful hostile mutations were rejected: removing or narrowing the
  level guard, lowering the finite boundary, bypassing either helper call, and
  restoring either integer origin shift.
- Independent review found and closed non-finite assertion and zero-extent
  gaps. Hosted validation and exact-head review evidence are recorded in the
  change log before merge.
