---
title: Smartclip Empty Geometry Boundary
date: 2026-06-25
type: implementation-plan
status: completed
---

# Smartclip Empty Geometry Boundary

## Problem

`smartclip.Polygon` passed empty inner rings to `clipRings`, which indexed their
first and last points. `smartclip.MultiPolygon` also indexed the outer ring of
every child polygon without checking whether the polygon or outer ring was
empty. Malformed geometry therefore caused index-out-of-range panics before
valid sibling polygons could be clipped.

## Requirements

- Reject a polygon whose outer ring is empty instead of promoting a later ring.
- Ignore empty inner rings while preserving the valid outer and non-empty holes.
- Ignore empty child polygons and child polygons with empty outer rings in a
  multipolygon while preserving valid siblings.
- Keep well-formed clipping behavior and public signatures unchanged.
- Preserve compatibility with Go 1.20.

## Verification

- RED: Go 1.20.14 reproduced index-out-of-range panics for an empty inner ring,
  an empty outer ring, and empty multipolygon children.
- Focused regressions cover empty outer, empty inner, and empty child polygons.
- The full Smartclip package passes on Go 1.20.14.
- Full `make check` passes on Go 1.20.14 and Go 1.25.11, including tests,
  race detection, vet, workflow contracts, the static baseline, and Make-root
  isolation tests.
- The Codex review helper targeted `origin/master` but was skipped after the
  configured service returned repeated HTTP 401 authentication failures.
- The static baseline requires the normalization boundary, focused regressions,
  this completed plan, and synchronized public safety documentation.
