#!/usr/bin/env python3
"""Static baseline checks for the orb Go geometry library."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-orb-go-module-baseline.md"
HOSTED_VALIDATION_PLAN = "docs/plans/2026-06-10-hosted-go-validation.md"
REQUIRED = [
    ".github/workflows/check.yml",
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "docs/readme-overview.svg",
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
    "scripts/check-baseline.py",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


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

    go_sum = read("go.sum")
    for phrase in ["github.com/gogo/protobuf v1.3.2", "github.com/pkg/errors v0.9.1"]:
        if phrase not in go_sum:
            failures.append(f"go.sum must include {phrase}")

    makefile = read("Makefile")
    for phrase in [
        "go test ./...",
        "go test -race ./...",
        "go vet ./...",
        "python3 scripts/check-baseline.py",
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

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
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
        "race detector",
        "hosted Linux",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

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
    hosted_validation_plan = read(HOSTED_VALIDATION_PLAN)
    workflow = read(".github/workflows/check.yml")
    if "status: completed" not in hosted_validation_plan or "go test -race ./..." not in hosted_validation_plan:
        failures.append("hosted Go validation plan must record completed status and race verification")
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 15",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-go@4a3601121dd01d1626a1e23e37211e3254c1c06c",
        'go-version: ["1.20.14", "1.25.3"]',
        "GOTOOLCHAIN: local",
        "run: make check",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")

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
