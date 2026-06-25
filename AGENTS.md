# AGENTS.md

## Repository purpose

`garethpaul/orb` is a Go project. The checked-in files describe a Go project with the structure summarized below.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `go.mod` - Go module definition
- `clip` - repository source or sample assets
- `encoding` - repository source or sample assets
- `geo` - repository source or sample assets
- `geojson` - repository source or sample assets
- `internal` - repository source or sample assets
- `maptile` - repository source or sample assets
- `planar` - repository source or sample assets
- `project` - repository source or sample assets

## Development commands

- Install dependencies: `go mod download`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Go test all packages: `go test ./...`
- Go vet all packages: `go vet ./...`
- Go build all packages: `go build ./...`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Go (88).
- Keep imports compatible with module path `github.com/paulmach/orb`.
- Preserve the declared Go 1.20 module baseline unless a deliberate compatibility migration is approved; validate with Go 1.20.14 and the patched Go 1.25.11 lane.
- Run gofmt on changed Go files and keep table-driven tests close to the package under change.

## Testing guidance

- Test-related files detected: `bound_test.go`, `clip/clip_test.go`, `clip/example_test.go`, `clip/helpers_test.go`, `clip/smartclip/around_bound_test.go`, `clip/smartclip/smart_test.go`, `clip/smartclip/util_test.go`, `clone_test.go`, `encoding/mvt/clip_test.go`, `encoding/mvt/example_test.go`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Mapbox. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- Never commit credentials, private keys, access tokens, or machine-local secret files.
- Mapbox Vector Tile support depends on generated protobuf code under `encoding/mvt/vectortile`; keep the `.proto`, generated `.pb.go`, and tests in sync.
- Degenerate rings and malformed geometry inputs should fail predictably rather than panic in caller pipelines.
- Empty line strings should remain safe for helper methods such as reverse.
- Nil geometries inside collections should be ignored by aggregate helpers.
- Empty bounds should remain identity values in bound union helpers.
- Empty line strings passed to interval resampling must return before invoking caller-provided distance functions.
- Resampling must reject nil callbacks, non-finite coordinates or distances, non-progressing spacing, and requests above the documented 64 MiB point-allocation budget before output allocation.
- Polygon distance indices must remain `-1` when no ring contains a segment.
- Tiles at `maptile.MaxZoom` are leaves; above-ceiling children must not wrap,
  above-ceiling descendant ranges use zero-coordinate sentinels, and tile-cover
  merge helpers must not index nonexistent siblings.
- Generated protobuf Go files are present; keep source `.proto`, generated files, and tests in sync.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
