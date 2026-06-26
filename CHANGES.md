# Changes

## 2026-06-25T19:15:00-0700 — P1 reliability — maptile fraction boundary

- Bug: `maptile.Fraction` overflowed to non-finite coordinates at zoom 1024 and
  above, while line and polygon tile covers could traverse unrepresentable zooms
  directly and consume unbounded CPU.
- Work: preserved fraction scales through zoom 1023, saturated larger exponents,
  saturated overflowing finite longitude products, and made every tile-cover
  entry point return empty above `maptile.MaxZoom` before dispatch or iteration.
- Validation: RED on Go 1.20.14 reproduced infinities and NaNs; focused fraction
  and excessive-cover regressions pass. Full `make check` and `go mod verify`
  pass on Go 1.20.14 and Go 1.25.11; seven meaningful hostile mutations are
  rejected. Three independent reviewers approve after findings were resolved;
  the required Codex review was attempted at `3ec9017` and skipped after HTTP
  401 authentication failure. Hosted evidence follows.

## 2026-06-25T19:16:00-0700 — P1 correctness — reject invalid MVT geometry components

### Summary

Fixed public MVT marshaling so nil, empty, or too-short geometry components
return contextual errors instead of panicking or emitting invalid commands.

### Work completed

- Added public `Marshal` regressions for nil geometry and every empty or
  too-short point, line, ring, polygon, and nested multi-geometry shape.
- Reproduced missing errors and index-out-of-range panics on Go 1.20.14.
- Centralized pre-encoding validation before command allocation or point access,
  including MVT minimum line and ring command counts.
- Preserved existing layer and feature error context without silently dropping
  malformed features or child components.
- Added design, implementation, static, and public guidance contracts.

### Threads

- Started: none.
- Continued: direct MVT malformed-input hardening after reviewing recent Orb
  smartclip and Mercator fixes.
- Stopped: none.

### Files changed

- `encoding/mvt/geometry.go` — validates encoded geometry shapes.
- `encoding/mvt/marshal_test.go` — covers the public panic/error boundary.
- `scripts/check-baseline.py` — preserves source, tests, plans, and guidance.
- `README.md`, `SECURITY.md`, `VISION.md`, and `AGENTS.md` — document the MVT
  error-return contract.
- `docs/plans/2026-06-25-mvt-empty-geometry-marshal-design.md` and
  `docs/plans/2026-06-25-mvt-empty-geometry-marshal.md` — record the decision
  and implementation steps.

### Validation

- Focused RED on Go 1.20.14 — reproduced two missing errors and five panics,
  then five additional missing errors for one-point lines and two-point rings.
- Focused and full `encoding/mvt` tests — passed on Go 1.20.14 and Go 1.25.11.
- Full `make check` and `go mod verify` — passed in pinned Go 1.20.14 and Go
  1.25.11 containers, including all packages, race tests, vet, workflow/static
  contracts, and Make-root isolation.
- Twelve isolated hostile mutations — rejected removal or weakening of the
  encoder call, nil guard, and every top-level or nested shape minimum.
- `git diff --check` — passed.
- Hosted Check runs `28212959729` and `28212963171` — passed on Go 1.20.14, Go
  1.25.3, and Go 1.25.11.
- CodeQL run `28212962853` — passed for actions, Go, and Python analysis.
- Codex review helper with `codex review --base origin/master` — blocked by
  local OpenAI API authentication (HTTP 401); exact-head manual review found no
  actionable findings.

### Bugs / findings

- P1: `mvt.Marshal` could panic caller pipelines on empty lines or rings and
  emit nonconformant commands for empty collections, one-point lines, and
  two-point rings.

### Blockers

- The host has no Go binary; pinned official Docker images provide local Go
  1.20.14 and Go 1.25.11 validation.
- Local Codex API authentication remains unavailable; exact-head manual review
  provided the review fallback.

### Next action

- Merge PR #22 after the final documentation-only head passes hosted checks.

## 2026-06-25T19:01:00-0700 — P1 correctness — smartclip empty geometry boundary

### Summary

Inspected all local open-source checkouts, avoided conflicting with concurrent
Dotfiles work, and fixed a reproducible Orb smart-clipping panic on malformed
empty polygon children.

### Work completed

- Rejected polygons whose outer ring is empty instead of indexing or promoting
  a later ring.
- Ignored empty inner rings and invalid multipolygon children while preserving
  valid sibling geometry.
- Added focused Go regressions, a completed implementation plan, public safety
  documentation, and mutation-sensitive static baseline checks.

### Threads

- Started: none.
- Continued: direct Orb malformed-geometry hardening.
- Stopped: Dotfiles supply-chain inspection after another process changed the
  shared checkout, avoiding duplicate or conflicting edits.

### Files changed

- `clip/smartclip/smart.go` — normalized polygon inputs before clipping.
- `clip/smartclip/smart_test.go` — covered empty outer, inner, and child geometry.
- `scripts/check-baseline.py` — preserved the new panic-resistance contract.
- `README.md`, `SECURITY.md`, `VISION.md` — documented malformed-input behavior.
- `docs/plans/2026-06-25-smartclip-empty-geometry.md` — recorded requirements and proof.

### Validation

- RED on Go 1.20.14 — reproduced index-out-of-range panics in all three focused cases.
- `go test ./clip/smartclip -count=1` on Go 1.20.14 — passed.
- `make check` on Go 1.20.14 — passed tests, race, vet, workflow, static, and root gates.
- `make check` on Go 1.25.11 — passed tests, race, vet, workflow, static, and root gates.
- Codex review helper against `origin/master` — skipped after repeated HTTP 401
  authentication failures; no review finding was produced.
- Hosted test lanes on Go 1.20.14, Go 1.25.3, and Go 1.25.11 — passed before
  this documentation-only evidence update.

### Bugs / findings

- P1: Smartclip indexed empty rings and empty child polygons before validation,
  allowing malformed geometry to panic caller pipelines.

### Blockers

- Codex review authentication is unavailable in this environment; skipped per
  the maintenance policy. This does not block hosted checks or merge.

### Next action

- Merge the focused pull request after this documentation-only update passes hosted checks.

## 2026-06-25T19:00:25-0700 — P1 correctness — cycle: Mercator projection scale boundary

- Cycle: inspected the public geometry library, recent zoom-boundary work,
  projection callers, numeric limits, tests, plans, and documented risks.
- Threads: used four read-only investigators to trace callers, historical
  contracts, numerical behavior, and regression strategy.
- Bug: Mercator levels at 1024 and above overflowed `math.Exp2` to infinity,
  while power-of-two MVT projection narrowed tile origins through `uint32`
  shifts and wrapped valid coordinates at zoom 21 and above.
- Work: centralized finite Mercator scaling through level 1023, saturated larger
  exponents at that finite boundary, replaced MVT origin shifts with
  `math.Ldexp`, defaulted explicit zero extents before projection, and added
  high-level, high-zoom, non-finite, and zero-extent regressions plus static
  contracts and repository guidance.
- Files: changed `internal/mercator`, `encoding/mvt`, documentation, and the
  static baseline; added the completed Mercator projection scale plan.
- Validation: RED on Go 1.20.14 reproduced infinite coordinates, plausible
  incorrect inverse coordinates, and wrapped power-of-two MVT origins. Focused
  tests, full `make check`, and `go mod verify` pass on Go 1.20.14 and Go
  1.25.11; seven meaningful hostile mutations covering both scale consumers and
  both origin axes are rejected. Independent review found and closed non-finite
  assertion and zero-extent gaps, and three reviewers approve the corrected
  patch. The required Codex branch review was attempted at `0b1dc6c` and skipped
  after an HTTP 401 authentication failure; hosted evidence follows before merge.
- Findings: MVT intentionally derives finite projection levels above
  `maptile.MaxZoom`, so the numeric boundary is float64 exponent capacity rather
  than tile-coordinate capacity. Converting tile origins before scaling avoids
  integer narrowing while preserving the optimized projection path.
- Blockers: the host has no Go binary, so validation uses pinned official Docker
  images.
- Next: complete exact-head review and confirm hosted validation before merge.

## 2026-06-25T18:01:05-0700 — P1 correctness — cycle: tile-cover minimum boundary

- Cycle: inspected the public geometry library, recent merge work, hosted checks,
  repository contracts, callers, tests, plans, and documented boundary risks.
- Threads: continued direct tile-cover boundary hardening; started or stopped none.
- Bug: `MergeUp` and `MergeUpPartial` returned an empty set when the requested
  minimum zoom exceeded the uniform input zoom because their loops performed no
  work after an equality-only no-op guard.
- Work: made both variants preserve the original set whenever `min >= inputZoom`,
  centralized uniform representable-zoom validation before sibling indexing,
  added complete and partial regressions, and extended the static test contract.
- Files: changed `maptile/tilecover/merge.go`,
  `maptile/tilecover/merge_test.go`, `scripts/check-baseline.py`, and added the
  tile-cover minimum-boundary implementation plan.
- Validation: RED on Go 1.20.14 returned `map[]` for both variants. Focused GREEN,
  static baseline, and complete `make check` gates pass on Go 1.20.14 and Go
  1.25.11; four hostile mutations removing either minimum guard, excessive-zoom
  rejection, or mixed-zoom rejection are rejected. Three independent reviewers
  approve, and both hosted Go matrices plus all CodeQL lanes pass at `710fcc2`.
- Findings: a merge target numerically above the source zoom requires subdivision,
  not merging, so identity is the only contract-compatible result. Unsupported
  mixed-zoom sets must also fail closed before unordered iteration reaches an
  unrepresentable sibling lookup.
- Blockers: the host has no Go binary, so validation uses pinned official Docker
  images; initial network-isolated runs found cold module caches and full gates
  then passed with dependency access. The required Codex review helper was
  attempted and skipped after an HTTP 401 authentication failure.
- Next: merge the clean pull request after final documentation-only checks pass.

## 2026-06-25T16:12:08-0700 — P1 correctness — cycle: maptile descendant ceiling

- Cycle: inspected the MIT-licensed geometry library, open work, hosted checks,
  recent zoom-32 repair, tile APIs, tests, plans, and documented follow-up risks.
- Threads: continued direct maptile boundary hardening; started or stopped none.
- Bug: `Tile.Children` shifted `uint32` coordinates past `MaxZoom`, producing
  wrapped invalid children, while `Tile.Range` retained wrapped payload
  coordinates for unrepresentable target zooms.
- Work: made maximum-zoom tiles leaf nodes and above-ceiling ranges return
  canonical invalid zero-coordinate endpoints; made complete and partial
  tile-cover merging preserve above-ceiling sets without sibling indexing.
- Files: changed `maptile/tile.go`, `maptile/tile_test.go`, repository guidance,
  `scripts/check-baseline.py`, and the completed descendant-boundary plan.
- Validation: RED on Go 1.20.14 showed wrapped maximum-zoom children and
  noncanonical invalid ranges. A first invalid-source guard then broke Fiji
  tile-cover merging and was reverted. Full offline `make check` passes on Go
  1.20.14 and Go 1.25.11, including tests, race, vet, workflow, baseline, and
  Make authority. Exact-head review then reproduced an above-ceiling `MergeUp`
  panic; after guarding both merge variants, the complete two-version gates
  pass again and six hostile boundary mutations, including removal of either
  merge guard, are rejected. Exact-head Codex review at `0ecd00c` reported no
  actionable findings, and both hosted test matrices plus all CodeQL lanes
  passed.
- Findings: `MaxZoom` must bound descendant construction as well as projection;
  invalidity by zoom alone does not prevent callers from consuming wrapped X/Y,
  and callers that expect four siblings must reject unrepresentable levels.
- Blockers: no local Go binary; cached network-isolated Go containers provide
  local validation, with hosted CI required for the repository's exact matrix.
- Next: merge the clean pull request and persist the cycle evidence.

## 2026-06-25T20:30:44Z — P1 correctness — cycle: maptile zoom boundary

- Threads: inspected the default branch, recent pull requests, hosted checks,
  repository contracts, projection helpers, tile arithmetic, and existing
  boundary coverage; no open pull requests or issues were present.
- Bug fixed: preserved the `2^32` Web Mercator scale instead of narrowing it
  to zero, restoring zoom-32 tile validation, point projection, bounds, and
  scalar Mercator round trips; tile coordinates now clamp before conversion so
  the eastern boundary cannot wrap in direct or tile-cover projection, and
  inclusive bound-cover loops terminate before `uint32` wraparound; zooms above
  the coordinate capacity produce invalid `At` tiles.
- Files: `maptile/tile.go`, `maptile/tile_test.go`,
  `maptile/tilecover/line_string.go`, `maptile/tilecover/cover_test.go`,
  `maptile/tilecover/helpers.go`,
  `internal/mercator/mercator.go`, and `internal/mercator/mercator_test.go`.
- Validation: reproduced four zoom-32 failures on Go 1.20.14, then passed all
  tests, race tests, and vet on Go 1.20.14 and Go 1.25.11 plus static baseline,
  hosted-workflow contract, and Make root contract checks.
- Blockers: the host has no Go executable, so validation used pinned official
  Docker images; no implementation or release blocker remains.
- Next: define compatibility semantics for `Children`, `Range`, and internal
  Mercator calls above the representable tile zoom before changing them.

## 2026-06-21

- Made absolute Makefile verification safe for spaces and apostrophes,
  ignored caller-provided `REPO_ROOT` values, and rejected command-line or
  environment `MAKEFILE_LIST` injection before Go gates run.
- Added root-policy regressions for every public Make target.

## 2026-06-19

- Bounded resampling output allocations to 64 MiB of points and rejected nil
  distance callbacks, non-finite coordinates, and non-progressing sample spacing.
- Switched interpolation to a finite overflow-safe weighted form and added
  deterministic property coverage for point counts, endpoints, and progress.
- Kept polygon distance indices at `-1` when no ring contains a segment.

## 2026-06-15

- Rejected nonfinite or integer-overflowing derived `ToInterval` point counts
  before integer conversion and output allocation.
- Rejected negative derived point counts from invalid distance callbacks before
  conversion and allocation.
- Rejected non-finite callback distances and callback-derived cumulative totals
  before either resampling entry point interpolates or allocates output points.
- Rejected negative callback segment distances before accumulation in both
  resampling entry points.
- Rejected a zero callback total before either resampling path interpolates while
  preserving mixed zero-length and positive callback segments.

## 2026-06-14

- Rejected non-finite `resample.ToInterval` distances before distance callback
  execution or point-count conversion, preventing a `NaN`-driven panic.
- Added regression and static contract coverage for `NaN` and both infinities.

## 2026-06-13

- Made every standard Make gate resolve Go module and checker paths from the
  repository root, including absolute-Makefile calls from external directories.
- Documented the Go 1.20 compatibility minimum, fixed 1.20.14 and patched 1.25.11
  validation roles, local-toolchain boundary, module-path stability,
  dependency-integrity checks, and generated protobuf expectations.

## 2026-06-12

- Disabled checkout credential persistence in the pinned, read-only hosted
  validation job and added structural checks for that boundary.
- Corrected `planar.DistanceFromWithIndex` for polygons to return the matching
  ring index instead of an outer or hole segment index.
- Added outer-ring, hole-ring, and empty-polygon regression coverage.

## 2026-06-09

- Made planar containment helpers treat empty rings and polygons as
  non-containing inputs instead of panicking.
- Covered `Bound.Union` empty argument behavior so empty bounds stay identity
  values on both sides of union operations.
- Added stable Make aliases for lint, build-through-test, and verify gates.
- Made multipolygon simplification skip empty polygon entries without panicking.
- Clarified and tested that zero-area bounds remain valid while malformed
  negative bounds are empty.

## 2026-06-10

- Added direct coverage that `MultiPolygon.Bound` skips leading empty polygons
  when aggregating child bounds.
- Added the Go race detector to the canonical verification gate.
- Added pinned hosted Linux validation on Go 1.20.14 and Go 1.25.3.
- Pinned checkout to its Node.js 24-compatible release before the hosted
  Node.js 20 action runtime removal.
- Guarded empty line strings in `resample.ToInterval` before distance
  precomputation and callback execution.

## 2026-06-08

- Added a Go module for the existing `github.com/paulmach/orb` import path.
- Pinned the protobuf and error helper dependencies used by MVT encoding.
- Added `make check` and static baseline verification.
- Added `go vet ./...` to the `make check` verification gate.
- Guarded degenerate rings so short rings are not treated as closed and
  orientation checks return zero instead of panicking.
- Made `LineString.Reverse` tolerate empty line strings without panicking.
- Made `Collection.Dimensions` skip nil geometries instead of panicking.
- Made `Bound.Union` treat an empty receiver as an identity value.
- Added local ignore rules for secrets, logs, Go test binaries, coverage
  output, and temporary build artifacts.
- Documented the module path, Mapbox Vector Tile generated source, and testdata
  baseline.
