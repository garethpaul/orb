# Security Policy

## Supported Versions

The supported security scope for `orb` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: No GitHub description is currently set.

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/orb` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a public sample, documentation, or utility project. The active security scope is the code and documentation on the default branch.
- Review found external API integrations or credential-adjacent configuration; changes in those areas should receive security-focused review before merge.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found mobile permission or privacy-sensitive data handling; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- Review found database, model, query, or persistence-related code; changes in those areas should receive security-focused review before merge.
- Dependency manifests detected: go.mod, go.sum. Dependency updates should keep
  module checksums in sync and preserve repeatable `go test ./...` behavior.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

For this geometry library, also review malformed GeoJSON, WKB/WKT, and Mapbox
Vector Tile inputs for panics, excessive allocation, coordinate-order mistakes,
and projection edge cases. Run `make check`, `make lint`, `make build`,
`make verify`, and `go test ./...` before changing parsers, encoders, generated
protobuf code, or fixture data.
The canonical gate also runs the Go race detector, and pinned hosted Linux jobs
use credential-free checkout while exercising both the declared Go 1.20
baseline and the patched Go 1.25.11 toolchain.
The Go support contract requires `GOTOOLCHAIN=local`, no checked-in `toolchain`
directive, synchronized module checksums, `go mod verify`, and review of direct
and transitive dependency changes on both fixed toolchains.
Degenerate rings should remain panic-resistant because geometry libraries are
often used in data pipelines that receive malformed input.
Empty line strings should also remain panic-resistant in helper methods such as
reverse.
Empty bounds should remain identity values when aggregate helpers union child
geometry bounds.
Zero-area bounds should remain valid so point and segment extents are not
misclassified as malformed empty bounds.
Empty polygons inside multipolygons should remain panic-resistant in
simplification helpers.
Simplification must not return polygons whose exterior ring collapses below
the minimum usable polygon boundary.
Smart clipping should reject polygons with empty outer rings and ignore empty
inner rings or child polygons rather than indexing malformed geometry.
MVT marshaling should return contextual errors for nil, empty, or too-short
geometry components and for line or ring vertices that collapse to zero-length
encoded segments instead of panicking or emitting invalid commands.
WKB element-count loops should retain the decoded `uint32` type so malformed
high-bit counts cannot truncate through architecture-sized `int` and bypass
payload reads on 32-bit builds.
Leading empty polygons should remain safe in multipolygon bound aggregation so
aggregate bounds do not leak malformed empty-bound sentinels.
Collection simplification should remove nil and collapsed children so callers
do not receive stale nil geometry slots after validating the simplified result.
Empty interval resampling should return before allocating segment distances or
calling caller-provided distance functions.
Non-finite interval distances should be rejected before distance callbacks or
point-count conversion so malformed numeric input cannot trigger a panic or
unexpected allocation.
Derived point counts for resampling should be rejected before conversion or
allocation when interval division is nonfinite or exceeds the platform integer
range.
Negative derived point counts from caller distance callbacks should fail closed
before conversion or allocation.
Non-finite callback distances and callback-derived cumulative totals should
fail closed before either resampling path interpolates or allocates output points.
Negative callback segment distances should fail closed before accumulation so
later positive segments cannot mask invalid cumulative geometry.
A zero callback total should fail closed before `Resample` interpolation so a
malformed distance callback cannot prevent forward progress.
Descendant tile operations must not wrap coordinates beyond `maptile.MaxZoom`;
maximum-zoom tiles have no children, and above-ceiling ranges use a canonical
zero-coordinate sentinel. Tile-cover merge helpers preserve above-ceiling sets
without traversing nonexistent siblings.
Mercator scale exponents must remain finite, and power-of-two MVT projection
must not narrow high-zoom tile origins through `uint32` shifts. Zero MVT extents
must use the default extent before projection.
Direct tile fractions must remain finite at excessive zooms, and line or polygon
tile-cover traversal must stop before unrepresentable zooms can consume CPU.
Nil callbacks, non-finite coordinates, underflowing sample spacing, and point
requests above the 64 MiB resampling output budget should fail closed before
allocation or interpolation.
Empty rings and polygons should remain panic-resistant in planar containment
helpers.
Polygon distance indices should identify the matching immediate ring rather
than an internal segment; polygons without usable segments should return index
`-1` so callers do not select unrelated geometry.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
