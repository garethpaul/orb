#!/usr/bin/env python3
"""Static baseline checks for the orb Go geometry library."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-orb-go-module-baseline.md"
HOSTED_VALIDATION_PLAN = "docs/plans/2026-06-10-hosted-go-validation.md"
POLYGON_DISTANCE_INDEX_PLAN = "docs/plans/2026-06-12-polygon-distance-ring-index.md"
CHECKOUT_CREDENTIAL_PLAN = "docs/plans/2026-06-12-checkout-credential-boundary.md"
GO_SUPPORT_PLAN = "docs/plans/2026-06-13-go-support-contract.md"
PATCHED_MODERN_LANE_PLAN = "docs/plans/2026-06-13-patched-modern-go-lane.md"
LOCATION_INDEPENDENT_MAKE_PLAN = "docs/plans/2026-06-13-location-independent-make-gates.md"
REQUIRED = [
    ".github/workflows/check.yml",
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "docs/readme-overview.svg",
    "docs/go-support.md",
    "go.mod",
    "go.sum",
    PLAN,
    "docs/plans/2026-06-09-degenerate-ring-guards.md",
    "docs/plans/2026-06-09-empty-linestring-reverse.md",
    "docs/plans/2026-06-09-collection-dimensions-nil.md",
    "docs/plans/2026-06-09-empty-bound-union.md",
    "docs/plans/2026-06-09-empty-bound-union-argument.md",
    "docs/plans/2026-06-09-simplify-empty-multipolygon.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-planar-empty-containment.md",
    "docs/plans/2026-06-09-zero-area-bound-contract.md",
    "docs/plans/2026-06-10-multipolygon-empty-bound.md",
    "docs/plans/2026-06-10-resample-empty-interval.md",
    HOSTED_VALIDATION_PLAN,
    POLYGON_DISTANCE_INDEX_PLAN,
    CHECKOUT_CREDENTIAL_PLAN,
    GO_SUPPORT_PLAN,
    PATCHED_MODERN_LANE_PLAN,
    LOCATION_INDEPENDENT_MAKE_PLAN,
    "scripts/check-baseline.py",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def main():
    failures = []
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"required file missing: {path}")

    go_mod = read("go.mod")
    for phrase in [
        "module github.com/paulmach/orb",
        "go 1.20",
        "github.com/gogo/protobuf v1.3.2",
        "github.com/pkg/errors v0.9.1",
    ]:
        if phrase not in go_mod:
            failures.append(f"go.mod must include {phrase}")
    if re.search(r"(?m)^toolchain\s+", go_mod):
        failures.append("go.mod must not force an automatic toolchain switch")

    go_sum = read("go.sum")
    for phrase in ["github.com/gogo/protobuf v1.3.2", "github.com/pkg/errors v0.9.1"]:
        if phrase not in go_sum:
            failures.append(f"go.sum must include {phrase}")

    makefile = read("Makefile")
    for phrase in [
        "override REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))",
        'cd "$(REPO_ROOT)" && go test ./...',
        'cd "$(REPO_ROOT)" && go test -race ./...',
        'cd "$(REPO_ROOT)" && go vet ./...',
        'python3 "$(REPO_ROOT)/scripts/check-baseline.py"',
        "check: test race lint static-check",
        "lint: vet",
        "build: test",
        "verify: check",
    ]:
        if phrase not in makefile:
            failures.append(f"Makefile must include {phrase}")

    gitignore = read(".gitignore")
    for phrase in [".env", "*.test", "coverage.out", "tmp/"]:
        if phrase not in gitignore:
            failures.append(f".gitignore must include {phrase}")

    for path in [
        "encoding/mvt/vectortile/vector_tile.proto",
        "encoding/mvt/vectortile/vector_tile.pb.go",
        "encoding/mvt/testdata/15-8956-12223.mvt",
        "maptile/tilecover/testdata/world.geojson",
    ]:
        if not (ROOT / path).is_file():
            failures.append(f"fixture or generated source missing: {path}")

    testdata_count = sum(1 for _ in (ROOT / "maptile/tilecover/testdata").rglob("*") if _.is_file())
    if testdata_count < 300:
        failures.append("tilecover testdata fixture set unexpectedly small")

    ring = read("ring.go")
    for phrase in ["if len(r) < 4", "if len(r) < 3"]:
        if phrase not in ring:
            failures.append(f"ring.go must guard degenerate rings with {phrase}")
    line_string = read("line_string.go")
    if "for i, j := 0, len(ls)-1; i < j; i, j = i+1, j-1" not in line_string:
        failures.append("LineString.Reverse must tolerate empty line strings")
    line_string_tests = read("line_string_test.go")
    if "empty line string" not in line_string_tests:
        failures.append("line string tests must cover empty reverse")
    geometry = read("geometry.go")
    geometry_tests = read("geometry_test.go")
    if "if g == nil" not in geometry or "continue" not in geometry:
        failures.append("Collection.Dimensions must skip nil geometries")
    if "TestCollectionDimensionsSkipsNilGeometries" not in geometry_tests or "nil geometry collection dimensions" not in geometry_tests:
        failures.append("geometry tests must cover nil collection dimensions")
    ring_tests = read("ring_test.go")
    for phrase in [
        "empty ring is not closed",
        "too-short ring is not closed even when endpoints match",
        "TestRing_OrientationDegenerate",
        "collinear ring",
    ]:
        if phrase not in ring_tests:
            failures.append(f"ring tests must include {phrase}")
    bound = read("bound.go")
    bound_tests = read("bound_test.go")
    multi_line_tests = read("multi_line_string_test.go")
    multi_polygon_tests = read("multi_polygon_test.go")
    if "if b.IsEmpty()" not in bound or "return other" not in bound:
        failures.append("Bound.Union must return the other bound when the receiver is empty")
    if "TestBoundUnionWithEmptyReceiver" not in bound_tests:
        failures.append("bound tests must cover empty receiver union")
    if "TestBoundUnionWithEmptyArgument" not in bound_tests:
        failures.append("bound tests must cover empty argument union")
    if "Zero-area bounds" not in bound:
        failures.append("Bound.IsEmpty docs must clarify zero-area bound behavior")
    for phrase in ["single point", "horizontal zero-area bound", "vertical zero-area bound"]:
        if phrase not in bound_tests:
            failures.append(f"bound tests must cover {phrase}")
    if "TestMultiLineString_BoundSkipsLeadingEmptyLineString" not in multi_line_tests:
        failures.append("multi line string tests must cover leading empty bounds")
    if "TestMultiPolygon_BoundSkipsLeadingEmptyPolygon" not in multi_polygon_tests:
        failures.append("multi polygon tests must cover leading empty polygon bounds")
    resample = read("resample/line_string.go")
    resample_tests = read("resample/line_string_test.go")
    interval_start = resample.find("func ToInterval")
    interval_guard = resample.find("if len(ls) <= 1", interval_start)
    distance_setup = resample.find("total, dists := precomputeDistances(ls, df)", interval_start)
    if interval_guard == -1 or distance_setup == -1 or interval_guard > distance_setup:
        failures.append("ToInterval must guard empty line strings before distance precomputation")
    if "TestToIntervalEmptyLineString" not in resample_tests or "distance function should not be called" not in resample_tests:
        failures.append("resample tests must cover empty interval input before distance calls")
    distance_from = read("planar/distance_from.go")
    distance_from_tests = read("planar/distance_from_test.go")
    for phrase in [
        "index of the immediate child",
        "dist, _ := lineStringDistanceFrom(orb.LineString(p[0]), point)",
        "index := 0",
        "d, _ := lineStringDistanceFrom(orb.LineString(p[i]), point)",
        "index = i",
    ]:
        if phrase not in distance_from:
            failures.append(f"polygon distance ring index must include {phrase}")
    for phrase in [
        "TestDistanceFromWithIndex_PolygonReturnsRingIndex",
        "outer ring nearest on nonzero segment",
        "hole ring nearest on different segment",
        "TestDistanceFromWithIndex_EmptyPolygon",
    ]:
        if phrase not in distance_from_tests:
            failures.append(f"polygon distance tests must include {phrase}")
    simplify_helpers = read("simplify/helpers.go")
    simplify_tests = read("simplify/helpers_test.go")
    if "len(p) == 0" not in simplify_helpers or "len(p[0]) <= 2" not in simplify_helpers:
        failures.append("simplify multiPolygon must skip empty polygons before indexing")
    if "TestMultiPolygonSkipsEmptyPolygon" not in simplify_tests:
        failures.append("simplify tests must cover empty polygons inside multipolygons")
    planar_contains = read("planar/contains.go")
    planar_contains_tests = read("planar/contains_test.go")
    if "if len(r) == 0" not in planar_contains or "if len(p) == 0" not in planar_contains:
        failures.append("planar containment helpers must guard empty rings and polygons")
    for phrase in [
        "TestRingContainsEmptyRing",
        "TestPolygonContainsEmptyPolygon",
        "TestMultiPolygonContainsSkipsEmptyPolygons",
    ]:
        if phrase not in planar_contains_tests:
            failures.append(f"planar containment tests must include {phrase}")

    docs = " ".join(
        "\n".join(
            read(path)
            for path in ["README.md", "SECURITY.md", "VISION.md", "docs/go-support.md"]
        ).split()
    )
    for phrase in [
        "make check",
        "make lint",
        "make build",
        "make verify",
        "go test ./...",
        "go vet ./...",
        "github.com/paulmach/orb",
        "Go module",
        "Mapbox Vector Tile",
        "degenerate rings",
        "empty line strings",
        "nil geometries",
        "empty bounds",
        "empty union arguments",
        "empty polygons inside multipolygons",
        "empty rings and polygons",
        "zero-area bounds",
        "leading empty polygons",
        "empty interval resampling",
        "polygon ring index",
        "race detector",
        "hosted Linux",
        "Go compatibility minimum",
        "modern-toolchain validation",
        "GOTOOLCHAIN=local",
        "go mod verify",
        "breaking import migration",
        "generated Go source",
        "absolute Makefile path works from another directory",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    go_support = " ".join(read("docs/go-support.md").split())
    for phrase in [
        "Review date: 2026-06-13",
        "Go 1.20 is therefore the language and module compatibility minimum",
        "fixed Go 1.20.14 lane",
        "fixed Go 1.25.11 lane is patched modern-toolchain validation",
        "does not raise the declared minimum",
        "GOTOOLCHAIN=local",
        "intentionally has no `toolchain` directive",
        "github.com/paulmach/orb",
        "breaking import migration",
        "go.mod` and `go.sum` synchronized",
        "go mod verify",
        "direct and transitive graph changes",
        "generated Go source",
        "rather than hand-editing generated output",
        "both fixed Go 1.20.14 and Go 1.25.11 toolchains",
    ]:
        if phrase not in go_support:
            failures.append(f"Go support contract must include {phrase}")

    current_support_claims = {
        "README.md": [
            "Go 1.20.14 and Go 1.25.11",
            "Go 1.25.11 is patched modern-toolchain validation",
        ],
        "SECURITY.md": ["patched Go 1.25.11 toolchain"],
        "VISION.md": ["Go 1.20.14 and patched Go 1.25.11 validation"],
        "CHANGES.md": [
            "fixed 1.20.14 and patched 1.25.11 validation roles",
            "absolute-Makefile calls from external directories",
        ],
    }
    for path, phrases in current_support_claims.items():
        content = " ".join(read(path).split())
        for phrase in phrases:
            if phrase not in content:
                failures.append(f"{path} must include {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "go test ./..." not in plan or "go vet ./..." not in plan:
        failures.append("plan must record completed status and Go verification")
    ring_plan = read("docs/plans/2026-06-09-degenerate-ring-guards.md")
    if "status: completed" not in ring_plan or "go test ./..." not in ring_plan:
        failures.append("ring guard plan must record completed status and verification")
    line_plan = read("docs/plans/2026-06-09-empty-linestring-reverse.md")
    if "status: completed" not in line_plan or "LineString.Reverse" not in line_plan:
        failures.append("line string plan must record completed status and verification")
    collection_plan = read("docs/plans/2026-06-09-collection-dimensions-nil.md")
    if "status: completed" not in collection_plan or "Collection.Dimensions" not in collection_plan:
        failures.append("collection dimensions plan must record completed status and verification")
    empty_bound_plan = read("docs/plans/2026-06-09-empty-bound-union.md")
    if "status: completed" not in empty_bound_plan or "Bound.Union" not in empty_bound_plan:
        failures.append("empty bound union plan must record completed status and verification")
    empty_bound_argument_plan = read("docs/plans/2026-06-09-empty-bound-union-argument.md")
    if (
        "status: completed" not in empty_bound_argument_plan
        or "Bound.Union" not in empty_bound_argument_plan
        or "empty argument" not in empty_bound_argument_plan
    ):
        failures.append("empty bound union argument plan must record completed status and verification")
    simplify_plan = read("docs/plans/2026-06-09-simplify-empty-multipolygon.md")
    if "status: completed" not in simplify_plan or "multiPolygon" not in simplify_plan:
        failures.append("simplify empty multipolygon plan must record completed status and verification")
    aliases_plan = read("docs/plans/2026-06-09-make-gate-aliases.md")
    for phrase in ["status: completed", "make lint", "make build", "make verify"]:
        if phrase not in aliases_plan:
            failures.append(f"make gate alias plan must record {phrase}")
    planar_contains_plan = read("docs/plans/2026-06-09-planar-empty-containment.md")
    if "status: completed" not in planar_contains_plan or "RingContains" not in planar_contains_plan:
        failures.append("planar empty containment plan must record completed status and verification")
    zero_area_bound_plan = read("docs/plans/2026-06-09-zero-area-bound-contract.md")
    if "status: completed" not in zero_area_bound_plan or "zero-area bounds" not in zero_area_bound_plan:
        failures.append("zero-area bound plan must record completed status and verification")
    multipolygon_empty_bound_plan = read("docs/plans/2026-06-10-multipolygon-empty-bound.md")
    if (
        "status: completed" not in multipolygon_empty_bound_plan
        or "MultiPolygon.Bound" not in multipolygon_empty_bound_plan
        or "leading empty polygons" not in multipolygon_empty_bound_plan
    ):
        failures.append("multipolygon empty bound plan must record completed status and verification")
    resample_empty_plan = read("docs/plans/2026-06-10-resample-empty-interval.md")
    if "status: completed" not in resample_empty_plan or "ToInterval" not in resample_empty_plan:
        failures.append("empty interval resampling plan must record completed status and verification")
    polygon_distance_index_plan = read(POLYGON_DISTANCE_INDEX_PLAN)
    ring_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", polygon_distance_index_plan)
    ring_work = markdown_section(polygon_distance_index_plan, "Work Completed")
    ring_verification = markdown_section(polygon_distance_index_plan, "Verification Completed")
    if ring_status != ["completed"] or not ring_work:
        failures.append("polygon distance ring index plan must record one completed status and completed work")
    if not ring_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", ring_verification
    ):
        failures.append("polygon distance ring index plan must record completed verification")
    for evidence in [
        "GOTOOLCHAIN=go1.20.14 go test ./planar",
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.3 make check",
        "git diff --check",
        "python3 -m py_compile scripts/check-baseline.py",
        "27398396811",
        "27398401926",
        "dd2af0a49a33303c9336f67da7a39ac1c90a42f7",
        "TestDistanceFromWithIndex_PolygonReturnsRingIndex",
        "outer ring nearest on nonzero segment",
        "index: 0",
        "hole ring nearest on different segment",
        "index: 1",
        "TestDistanceFromWithIndex_EmptyPolygon",
        "+Inf",
        "-1",
    ]:
        if evidence not in ring_verification:
            failures.append(f"polygon distance ring-index verification must record {evidence}")
    hosted_validation_plan = read(HOSTED_VALIDATION_PLAN)
    workflow = read(".github/workflows/check.yml")
    workflow_files = [
        *sorted((ROOT / ".github/workflows").glob("*.yml")),
        *sorted((ROOT / ".github/workflows").glob("*.yaml")),
    ]
    if "status: completed" not in hosted_validation_plan or "go test -race ./..." not in hosted_validation_plan:
        failures.append("hosted Go validation plan must record completed status and race verification")
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 15",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-go@4a3601121dd01d1626a1e23e37211e3254c1c06c",
        'go-version: ["1.20.14", "1.25.11"]',
        "GOTOOLCHAIN: local",
        "run: make check",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")

    checkout_action = (
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
    )
    checkout_blocks = re.findall(
        rf"(?m)^(?P<indent> *)- +uses: +{re.escape(checkout_action)}[^\n]*\n"
        rf"(?P=indent)  with:\n"
        rf"(?P=indent)    persist-credentials: +false *$",
        workflow,
    )
    checkout_actions = re.findall(r"(?m)^\s*-\s+uses:\s+actions/checkout@", workflow)
    if not (
        len(workflow_files) == 1
        and workflow.count("permissions:") == 1
        and workflow.count("contents: read") == 1
        and not re.search(r"(?m)^\s*[A-Za-z-]+:\s*write\s*$", workflow)
        and len(checkout_actions) == 1
        and workflow.count(checkout_action) == 1
        and len(checkout_blocks) == 1
        and workflow.count("persist-credentials: false") == 1
        and "persist-credentials: true" not in workflow
    ):
        failures.append(
            "Check workflow must keep one read-only permission block and one "
            "pinned, credential-free checkout"
        )

    checkout_plan = read(CHECKOUT_CREDENTIAL_PLAN)
    checkout_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", checkout_plan)
    checkout_work = markdown_section(checkout_plan, "Work Completed")
    checkout_verification = markdown_section(checkout_plan, "Verification Completed")
    if not (
        checkout_status == ["completed"]
        and checkout_work
        and "make check" in checkout_verification
    ):
        failures.append(
            "checkout credential plan must record one completed status, "
            "completed work, and make check verification"
        )

    go_support_plan = read(GO_SUPPORT_PLAN)
    go_support_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", go_support_plan)
    go_support_work = markdown_section(go_support_plan, "Work Completed")
    go_support_verification = markdown_section(go_support_plan, "Verification Completed")
    if go_support_status != ["completed"] or not go_support_work:
        failures.append(
            "Go support plan must record one completed status and completed work"
        )
    if not go_support_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", go_support_verification
    ):
        failures.append("Go support plan must record completed verification")
    for evidence in [
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.3 make check",
        "GOTOOLCHAIN=go1.20.14 go mod verify",
        "GOTOOLCHAIN=go1.25.3 go mod verify",
        "external working directory",
        "workflow YAML",
        "hostile mutations rejected",
        "git diff --check",
        "secret and generated-artifact scan",
    ]:
        if evidence not in go_support_verification:
            failures.append(f"Go support verification must record {evidence}")

    patched_lane_plan = read(PATCHED_MODERN_LANE_PLAN)
    patched_lane_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", patched_lane_plan)
    patched_lane_work = markdown_section(patched_lane_plan, "Work Completed")
    patched_lane_verification = markdown_section(patched_lane_plan, "Verification Completed")
    if patched_lane_status != ["completed"] or not patched_lane_work:
        failures.append(
            "patched modern Go lane plan must record one completed status and completed work"
        )
    if not patched_lane_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", patched_lane_verification
    ):
        failures.append("patched modern Go lane plan must record completed verification")
    for evidence in [
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.11 make check",
        "GOTOOLCHAIN=go1.20.14 go mod verify",
        "GOTOOLCHAIN=go1.25.11 go mod verify",
        "govulncheck",
        "workflow YAML",
        "hostile mutations",
        "git diff --check",
    ]:
        if evidence not in patched_lane_verification:
            failures.append(f"patched modern Go lane verification must record {evidence}")

    location_make_plan = read(LOCATION_INDEPENDENT_MAKE_PLAN)
    location_make_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", location_make_plan
    )
    location_make_work = markdown_section(location_make_plan, "Work Completed")
    location_make_verification = markdown_section(
        location_make_plan, "Verification Completed"
    )
    if location_make_status != ["completed"] or not location_make_work:
        failures.append(
            "location-independent Make plan must record one completed status "
            "and completed work"
        )
    if not location_make_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", location_make_verification
    ):
        failures.append(
            "location-independent Make plan must record completed verification"
        )
    for evidence in [
        "make test",
        "make race",
        "make lint",
        "make build",
        "make static-check",
        "make verify",
        "make check",
        "GOTOOLCHAIN=go1.20.14",
        "GOTOOLCHAIN=go1.25.11",
        "from `/tmp`",
        "absolute",
        "caller-supplied",
        "REPO_ROOT=/tmp",
        "GOTOOLCHAIN=go1.20.14 go mod verify",
        "GOTOOLCHAIN=go1.25.11 go mod verify",
        "python3 -m py_compile scripts/check-baseline.py",
        "workflow YAML parsed successfully",
        "Twelve isolated hostile mutations were rejected",
    ]:
        if evidence not in location_make_verification:
            failures.append(
                f"location-independent Make verification must record {evidence}"
            )

    try:
        ET.parse(ROOT / "docs/readme-overview.svg")
    except ET.ParseError as error:
        failures.append(f"docs/readme-overview.svg must parse as XML: {error}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("orb Go module baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
