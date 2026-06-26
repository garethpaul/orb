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
SAFE_MAKE_ROOT_PLAN = "docs/plans/2026-06-21-safe-make-root.md"
NONFINITE_INTERVAL_PLAN = "docs/plans/2026-06-14-nonfinite-resample-interval.md"
DERIVED_POINT_COUNT_PLAN = "docs/plans/2026-06-15-derived-point-count-guard.md"
NEGATIVE_POINT_COUNT_PLAN = "docs/plans/2026-06-15-negative-derived-point-count.md"
NONFINITE_CALLBACK_PLAN = "docs/plans/2026-06-15-nonfinite-callback-distance.md"
NEGATIVE_CALLBACK_SEGMENT_PLAN = "docs/plans/2026-06-15-negative-callback-segment-distance.md"
ZERO_CALLBACK_TOTAL_PLAN = "docs/plans/2026-06-15-zero-callback-total.md"
RESAMPLE_DEGENERATE_FIXTURES_PLAN = "docs/plans/2026-06-26-resample-degenerate-public-fixtures.md"
MAPTILE_DESCENDANT_PLAN = "docs/plans/2026-06-25-maptile-descendant-boundary.md"
SMARTCLIP_EMPTY_GEOMETRY_PLAN = "docs/plans/2026-06-25-smartclip-empty-geometry.md"
MERCATOR_SCALE_PLAN = "docs/plans/2026-06-25-mercator-projection-scale-boundary.md"
MAPTILE_FRACTION_PLAN = "docs/plans/2026-06-25-maptile-fraction-boundary.md"
MVT_EMPTY_GEOMETRY_DESIGN = "docs/plans/2026-06-25-mvt-empty-geometry-marshal-design.md"
MVT_EMPTY_GEOMETRY_PLAN = "docs/plans/2026-06-25-mvt-empty-geometry-marshal.md"
MVT_ZERO_DELTA_DESIGN = "docs/plans/2026-06-25-mvt-zero-delta-design.md"
MVT_ZERO_DELTA_PLAN = "docs/plans/2026-06-25-mvt-zero-delta.md"
WKB_UINT32_COUNT_DESIGN = "docs/plans/2026-06-26-wkb-uint32-count-loops-design.md"
WKB_UINT32_COUNT_PLAN = "docs/plans/2026-06-26-wkb-uint32-count-loops.md"
SIMPLIFY_COLLAPSED_EXTERIOR_DESIGN = "docs/plans/2026-06-26-simplify-collapsed-exterior-design.md"
SIMPLIFY_COLLAPSED_EXTERIOR_PLAN = "docs/plans/2026-06-26-simplify-collapsed-exterior.md"
COLLECTION_BOUND_FIXTURES_PLAN = "docs/plans/2026-06-26-collection-bound-fixtures.md"
COLLECTION_CLIP_FIXTURE_PLAN = "docs/plans/2026-06-26-collection-clip-fixture.md"
SIMPLIFY_COLLECTION_COMPACTION_PLAN = "docs/plans/2026-06-26-simplify-collection-compaction.md"
EXPECTED_CHECK_WORKFLOW = """name: Check
on:
  pull_request:
  push:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        go-version: ["1.20.14", "1.25.3", "1.25.11"]
    env:
      GOTOOLCHAIN: local
    steps:
      - uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10
        with:
          persist-credentials: false
      - uses: actions/setup-go@4a3601121dd01d1626a1e23e37211e3254c1c06c
        with:
          go-version: ${{ matrix.go-version }}
          cache-dependency-path: go.sum
      - run: make check
"""
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
    MAPTILE_FRACTION_PLAN,
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
    SAFE_MAKE_ROOT_PLAN,
    NONFINITE_INTERVAL_PLAN,
    DERIVED_POINT_COUNT_PLAN,
    NEGATIVE_POINT_COUNT_PLAN,
    NONFINITE_CALLBACK_PLAN,
    NEGATIVE_CALLBACK_SEGMENT_PLAN,
    ZERO_CALLBACK_TOTAL_PLAN,
    RESAMPLE_DEGENERATE_FIXTURES_PLAN,
    MAPTILE_DESCENDANT_PLAN,
    SMARTCLIP_EMPTY_GEOMETRY_PLAN,
    MVT_EMPTY_GEOMETRY_DESIGN,
    MVT_EMPTY_GEOMETRY_PLAN,
    MVT_ZERO_DELTA_DESIGN,
    MVT_ZERO_DELTA_PLAN,
    WKB_UINT32_COUNT_DESIGN,
    WKB_UINT32_COUNT_PLAN,
    SIMPLIFY_COLLAPSED_EXTERIOR_DESIGN,
    SIMPLIFY_COLLAPSED_EXTERIOR_PLAN,
    COLLECTION_BOUND_FIXTURES_PLAN,
    COLLECTION_CLIP_FIXTURE_PLAN,
    SIMPLIFY_COLLECTION_COMPACTION_PLAN,
    "scripts/check-baseline.py",
    "tests/test_makefile_root.py",
    "tests/test_workflow_contract.py",
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
        "ifneq ($(origin MAKEFILE_LIST),file)",
        "$(error MAKEFILE_LIST must not be overridden)",
        "override REPO_ROOT := $(shell path=",
        "export REPO_ROOT",
        'CDPATH= cd -- "$$directory" && /bin/pwd -P)',
        'cd "$$REPO_ROOT" && go test ./...',
        'GOARCH=386 go test ./encoding/wkb',
        'cd "$$REPO_ROOT" && go test -race ./...',
        'cd "$$REPO_ROOT" && go vet ./...',
        'python3 "$$REPO_ROOT/scripts/check-baseline.py"',
        'python3 "$$REPO_ROOT/tests/test_workflow_contract.py"',
        'PYTHONDONTWRITEBYTECODE=1 python3 "$$REPO_ROOT/tests/test_makefile_root.py"',
        "check: test race lint static-check root-test",
        "static-check: workflow-contract",
        "lint: vet",
        "build: test",
        "verify: check",
    ]:
        if phrase not in makefile:
            failures.append(f"Makefile must include {phrase}")

    wkb_count_test = read("encoding/wkb/count_test.go")
    for phrase in [
        "TestHighBitElementCountsAreNotAcceptedAsEmpty",
        "0x80000000",
        "errors.Is(err, ErrNotWKB)",
    ]:
        if phrase not in wkb_count_test:
            failures.append(f"WKB count regression must include {phrase}")

    wkb_decoder_sources = "\n".join(
        read(path)
        for path in [
            "encoding/wkb/point.go",
            "encoding/wkb/line_string.go",
            "encoding/wkb/polygon.go",
            "encoding/wkb/collection.go",
        ]
    )
    if "int(num)" in wkb_decoder_sources:
        failures.append("WKB count loops must not narrow uint32 counts to int")
    if wkb_decoder_sources.count("for i := uint32(0); i < num; i++") != 6:
        failures.append("all six WKB count loops must iterate with uint32 indices")

    for path in ["AGENTS.md", "README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        if "WKB" not in read(path) or "uint32" not in read(path):
            failures.append(f"{path} must document architecture-safe WKB uint32 counts")

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

    smartclip = read("clip/smartclip/smart.go")
    smartclip_tests = read("clip/smartclip/smart_test.go")
    for phrase in [
        "p = normalizePolygon(p)",
        "if p = normalizePolygon(p); p != nil",
        "if len(p) == 0 || len(p[0]) == 0",
    ]:
        if phrase not in smartclip:
            failures.append(f"smartclip must normalize malformed polygons with {phrase}")
    for phrase in [
        "TestPolygonIgnoresEmptyInnerRing",
        "TestPolygonRejectsEmptyOuterRing",
        "TestMultiPolygonIgnoresEmptyChildren",
    ]:
        if phrase not in smartclip_tests:
            failures.append(f"smartclip tests must include {phrase}")
    smartclip_plan = read(SMARTCLIP_EMPTY_GEOMETRY_PLAN)
    for phrase in ["empty outer", "empty inner", "empty child polygons"]:
        if phrase not in smartclip_plan:
            failures.append(f"smartclip empty-geometry plan must document {phrase}")

    mvt_geometry = read("encoding/mvt/geometry.go")
    mvt_marshal_tests = read("encoding/mvt/marshal_test.go")
    for phrase in [
        "validateGeometryForEncoding(g)",
        "if g == nil",
        "line string must contain at least two points",
        "multi line string child %d must contain at least two points",
        "polygon ring %d must contain at least three points",
        "multi polygon child %d ring %d must contain at least three points",
    ]:
        if phrase not in mvt_geometry:
            failures.append(f"MVT geometry encoding must reject invalid components with {phrase}")
    for phrase in [
        "normalizeLineStringForEncoding",
        "normalizeRingForEncoding",
        "normalizeEncodedPoints",
        "encodedPointsEqual",
        "line string must contain at least two encoded vertices",
        "ring must contain at least three encoded vertices",
    ]:
        if phrase not in mvt_geometry:
            failures.append(f"MVT geometry encoding must reject degenerate segments with {phrase}")
    for phrase in [
        "TestMarshalRejectsInvalidGeometryComponents",
        'name: "nil geometry"',
        'name: "one-point multiline child"',
        'name: "two-point multipolygon ring"',
        "layer empty: feature 0: error encoding geometry",
    ]:
        if phrase not in mvt_marshal_tests:
            failures.append(f"MVT marshal tests must preserve {phrase}")
    for phrase in [
        "TestMarshalRejectsDegenerateEncodedSegments",
        'name: "quantized line vertex"',
        'name: "closed ring with two encoded vertices"',
        "TestMarshalAllowsRepeatedMultiPoints",
        "TestMarshalNormalizesRedundantEncodedVertices",
        "RemoveEmpty(1.0, 1.0)",
        "layer degenerate: feature 0: error encoding geometry",
    ]:
        if phrase not in mvt_marshal_tests:
            failures.append(f"MVT marshal tests must preserve degenerate-segment boundary {phrase}")

    mvt_empty_design = read(MVT_EMPTY_GEOMETRY_DESIGN)
    mvt_empty_plan = read(MVT_EMPTY_GEOMETRY_PLAN)
    for phrase in ["## Status: Accepted", "Do not silently drop features", "Vector Tile 2.1 specification"]:
        if phrase not in mvt_empty_design:
            failures.append(f"MVT empty-geometry design must document {phrase}")
    for phrase in [
        "## Status: Completed",
        "Twelve isolated hostile mutations were rejected",
        "28212959729",
        "28212962853",
    ]:
        if phrase not in mvt_empty_plan:
            failures.append(f"MVT invalid-geometry implementation plan must preserve {phrase}")
    mvt_zero_delta_design = read(MVT_ZERO_DELTA_DESIGN)
    mvt_zero_delta_plan = read(MVT_ZERO_DELTA_PLAN)
    for phrase in [
        "## Status: Accepted",
        "LineTo(0, 0)",
        "quantize to the same integer",
        "Normalize redundant encoded vertices, then reject collapsed geometry",
    ]:
        if phrase not in mvt_zero_delta_design:
            failures.append(f"MVT degenerate-segment design must document {phrase}")
    for phrase in [
        "## Status: Completed",
        "Compare coordinates after the encoder's `int32` conversion",
        "Reject lines and rings that collapse below their command-count minimums",
        "Twelve isolated hostile mutations were rejected",
        "28213260959",
        "28213261684",
    ]:
        if phrase not in mvt_zero_delta_plan:
            failures.append(f"MVT degenerate-segment implementation plan must preserve {phrase}")
    bound = read("bound.go")
    bound_tests = read("bound_test.go")
    geometry_tests = read("geometry_test.go")
    multi_line_tests = read("multi_line_string_test.go")
    multi_polygon_tests = read("multi_polygon_test.go")
    clip_helper_tests = read("clip/helpers_test.go")
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
    for test_name in [
        "TestCollectionBoundSkipsLeadingEmptyGeometry",
        "TestCollectionBoundIncludesNestedGeometryGroups",
    ]:
        if test_name not in geometry_tests:
            failures.append(f"collection bound fixtures must preserve {test_name}")
    collection_bound_plan = read(COLLECTION_BOUND_FIXTURES_PLAN)
    for phrase in [
        "Status: Completed",
        "leading empty geometry",
        "nested geometry groups",
        "No production source change was required",
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.11 make check",
        "Five isolated hostile mutations were rejected",
    ]:
        if phrase not in collection_bound_plan:
            failures.append(f"collection bound fixture plan must preserve {phrase}")
    if "Add aggregate-bound fixtures for leading empty polygons and geometry groups" in read("VISION.md"):
        failures.append("VISION must remove the completed aggregate-bound fixture priority")
    for phrase in [
        "Collection.Bound",
        "leading empty geometries",
        "nested geometry collections",
    ]:
        if phrase not in read("README.md"):
            failures.append(f"README must preserve collection bound fixture guidance: {phrase}")
    if "TestGeometryNestedCollectionKeepsSingleSurvivor" not in clip_helper_tests:
        failures.append("clip tests must preserve nested collection single-survivor coverage")
    collection_clip_plan = read(COLLECTION_CLIP_FIXTURE_PLAN)
    for phrase in [
        "Status: Completed",
        "nested collection",
        "single surviving point",
        "No production source change was required",
        "Go 1.20.14 and Go 1.25.11",
        "Four isolated hostile mutations were rejected",
    ]:
        if phrase not in collection_clip_plan:
            failures.append(f"collection clip fixture plan must preserve {phrase}")
    for phrase in [
        "Collection clipping recursively drops empty and outside children",
        "without a redundant collection wrapper",
    ]:
        if phrase not in read("README.md"):
            failures.append(f"README must preserve collection clipping guidance: {phrase}")
    resample = read("resample/line_string.go")
    resample_tests = read("resample/line_string_test.go")
    interval_start = resample.find("func ToInterval")
    finite_interval_guard = resample.find("if !validSpacing(dist)", interval_start)
    interval_guard = resample.find("if len(ls) <= 1", interval_start)
    distance_setup = resample.find("total, dists, ok := precomputeDistances(ls, df)", interval_start)
    point_count_setup = resample.find("pointCount := total / dist", distance_setup)
    point_count_guard = resample.find(
        "math.IsNaN(pointCount) || math.IsInf(pointCount, 0)", point_count_setup
    )
    point_count_conversion = resample.find("totalPoints := int(pointCount) + 1", point_count_setup)
    if not (
        0 <= finite_interval_guard < interval_guard < distance_setup
    ):
        failures.append(
            "ToInterval must reject non-finite distances before line handling "
            "and distance precomputation"
        )
    if interval_guard == -1 or distance_setup == -1 or interval_guard > distance_setup:
        failures.append("ToInterval must guard empty line strings before distance precomputation")
    resample_start = resample.find("func Resample")
    resample_distance_setup = resample.find(
        "total, dists, ok := precomputeDistances(ls, df)", resample_start
    )
    callback_guard = resample.find("if !ok", resample_distance_setup)
    interval_callback_guard = resample.find("if !ok", distance_setup)
    precompute_start = resample.find("func precomputeDistances")
    callback_validation = resample.find(
        "dists[i] < 0 || math.IsNaN(dists[i]) || math.IsInf(dists[i], 0)",
        precompute_start,
    )
    callback_accumulation = resample.find("total += dists[i]", callback_validation)
    callback_total_validation = resample.find(
        "math.IsNaN(total) || math.IsInf(total, 0)", callback_validation
    )
    if not (
        0 <= resample_distance_setup < callback_guard < interval_start
        and distance_setup < interval_callback_guard < point_count_setup
        and precompute_start < callback_validation < callback_accumulation
        < callback_total_validation
    ):
        failures.append(
            "both resample entry points must reject non-finite callback distances"
        )
    if not (
        distance_setup < point_count_setup < point_count_guard < point_count_conversion
        and "pointCount < 0" in resample
        and "pointCount >= float64(maxResamplePoints)" in resample
        and "maxResampleAllocationBytes = 64 << 20" in resample
    ):
        failures.append(
            "ToInterval must reject negative, non-finite, and int-overflowing derived point counts before conversion"
        )
    if "TestToIntervalEmptyLineString" not in resample_tests or "distance function should not be called" not in resample_tests:
        failures.append("resample tests must cover empty interval input before distance calls")
    for phrase in [
        "TestToIntervalRejectsNonFiniteDistance",
        "math.NaN()",
        "math.Inf(1)",
        "math.Inf(-1)",
        "distance function should not be called for non-finite intervals",
    ]:
        if phrase not in resample_tests:
            failures.append(
                f"resample tests must preserve non-finite interval coverage: {phrase}"
            )
    for phrase in [
        "TestResampleRejectsNonFiniteCallbackDistance",
        "non-finite callback distance should return nil from Resample",
        "non-finite callback distance should return nil from ToInterval",
        "finite cumulative overflow",
    ]:
        if phrase not in resample_tests:
            failures.append(
                f"resample tests must preserve non-finite callback coverage: {phrase}"
            )
    for phrase in [
        "TestResampleRejectsNegativeCallbackSegmentDistance",
        "negative callback segment should return nil from Resample",
        "negative callback segment should return nil from ToInterval",
        "return -1",
        "return 11",
    ]:
        if phrase not in resample_tests:
            failures.append(
                f"resample tests must preserve negative callback segment coverage: {phrase}"
            )
    for phrase in [
        "TestToIntervalRejectsNegativeDerivedPointCount",
        "return -planar.Distance(a, b)",
        "negative derived point count should return nil",
    ]:
        if phrase not in resample_tests:
            failures.append(
                f"resample tests must preserve negative derived point-count coverage: {phrase}"
            )
    for phrase in [
        "TestToIntervalRejectsUnrepresentablePointCount",
        "math.SmallestNonzeroFloat64",
        "unrepresentable point count should return nil",
    ]:
        if phrase not in resample_tests:
            failures.append(
                f"resample tests must preserve derived point-count coverage: {phrase}"
            )
    for phrase in [
        "TestResampleRejectsNilDistanceFunction",
        "TestResampleRejectsUnboundedPointCount",
        "TestResampleRejectsUnderflowedSpacing",
        "TestResampleKeepsFiniteCoordinatesFinite",
        "TestResampleStraightLineProperties",
    ]:
        if phrase not in resample_tests:
            failures.append(f"resample safety regression missing: {phrase}")
    distance_from = read("planar/distance_from.go")
    distance_from_tests = read("planar/distance_from_test.go")
    for phrase in [
        "index of the immediate child",
        "dist := math.Inf(1)",
        "index := -1",
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
        "TestDistanceFromWithIndex_PolygonWithoutSegments",
    ]:
        if phrase not in distance_from_tests:
            failures.append(f"polygon distance tests must include {phrase}")
    simplify_helpers = read("simplify/helpers.go")
    simplify_tests = read("simplify/helpers_test.go")
    if "len(p) == 0" not in simplify_helpers or "len(p[0]) <= 2" not in simplify_helpers:
        failures.append("simplify multiPolygon must skip empty polygons before indexing")
    if "TestMultiPolygonSkipsEmptyPolygon" not in simplify_tests:
        failures.append("simplify tests must cover empty polygons inside multipolygons")
    collection_helper = simplify_helpers.split("func collection", 1)[1].split(
        "func runSimplify", 1
    )[0]
    for phrase in ["count := 0", "if g == nil", "c[count] = g", "return c[:count]"]:
        if phrase not in collection_helper:
            failures.append(f"simplify collection must compact collapsed children: {phrase}")
    for test_name in [
        "TestCollectionSkipsCollapsedGeometries",
        "TestSimplifyCollectionReturnsNilWhenAllChildrenCollapse",
    ]:
        if test_name not in simplify_tests:
            failures.append(f"simplify collection regression missing: {test_name}")
    simplify_collection_plan = read(SIMPLIFY_COLLECTION_COMPACTION_PLAN)
    for phrase in [
        "Status: Completed",
        "[<nil> <nil> [5 6]]",
        "compact surviving geometries in place",
        "fully collapsed collection",
        "Ten isolated hostile mutations were rejected",
        "Go 1.20.14 and Go 1.25.11",
    ]:
        if phrase not in simplify_collection_plan:
            failures.append(f"simplify collection plan must preserve {phrase}")
    simplify_collection_guidance = {
        "README.md": "Collection simplification removes nil and collapsed children in place",
        "SECURITY.md": "Collection simplification should remove nil and collapsed children",
        "VISION.md": "Remove nil and collapsed children from simplified geometry collections",
        "AGENTS.md": "Collection simplification must compact nil and collapsed children",
    }
    for path, phrase in simplify_collection_guidance.items():
        if phrase not in read(path):
            failures.append(f"{path} must preserve simplified collection compaction guidance")
    polygon_helper = simplify_helpers.split("func polygon", 1)[1].split(
        "func multiPolygon", 1
    )[0]
    for phrase in ["if len(r) <= 2", "if i == 0", "return p[:0]"]:
        if phrase not in polygon_helper:
            failures.append(
                f"simplify polygon must drop a collapsed exterior ring: {phrase}"
            )
    for test_name in [
        "TestPolygonSkipsCollapsedExteriorRing",
        "TestPolygonDoesNotPromoteInteriorRing",
    ]:
        if test_name not in simplify_tests:
            failures.append(
                "simplify tests must cover collapsed polygon exteriors: "
                + test_name
            )
    tile_source = read("maptile/tile.go")
    tile_tests = read("maptile/tile_test.go")
    tile_merge_tests = read("maptile/tilecover/merge_test.go")
    for phrase in [
        "if t.Z >= MaxZoom",
        "if z > MaxZoom",
        "invalid := Tile{Z: z}",
    ]:
        if phrase not in tile_source:
            failures.append(f"maptile descendant boundary must include {phrase}")
    for phrase in ["const maxFiniteZoom Zoom = 1023", "if z > maxFiniteZoom", "finiteProduct(lng, maxtiles)", "math.MaxFloat64"]:
        if phrase not in tile_source:
            failures.append(f"maptile fraction boundary must include {phrase}")
    for phrase in ["zoom %d fraction should use the largest finite scale", "western fraction should remain finite", "excessive longitude should saturate"]:
        if phrase not in tile_tests:
            failures.append(f"maptile fraction tests must include {phrase}")
    for phrase in [
        "maximum zoom tile must not wrap into children",
        "last representable children must remain valid",
        "range above maximum zoom must be invalid",
    ]:
        if phrase not in tile_tests:
            failures.append(f"maptile descendant tests must include {phrase}")
    for phrase in [
        "TestMergeUpAboveMaximumZoom",
        "above-maximum tile must remain unchanged",
        "TestMergeUpPreservesSetWhenMinimumExceedsInputZoom",
        "minimum above input zoom must preserve the tile",
        "TestMergeUpPreservesNonuniformZoomSets",
        "nonuniform zoom set must remain unchanged",
    ]:
        if phrase not in tile_merge_tests:
            failures.append(f"tile-cover merge tests must include {phrase}")
    line_source = read("maptile/tilecover/line_string.go")
    helpers_source = read("maptile/tilecover/helpers.go")
    polygon_source = read("maptile/tilecover/polygon.go")
    cover_tests = read("maptile/tilecover/cover_test.go")
    if line_source.count("if z > maptile.MaxZoom") < 2 or "if zoom > maptile.MaxZoom" not in line_source:
        failures.append("line-based tile covers must reject excessive zooms before wrapper and internal traversal")
    if helpers_source.count("if z > maptile.MaxZoom") < 5:
        failures.append("tile-cover helpers must reject excessive zooms before dispatch and iteration")
    if polygon_source.count("if z > maptile.MaxZoom") < 3:
        failures.append("polygon tile-cover wrappers must reject excessive zooms before iteration")
    if "TestExcessiveZoomLineAndPolygonCovers" not in cover_tests:
        failures.append("tile-cover tests must cover excessive zoom traversal")

    mercator_source = read("internal/mercator/mercator.go")
    mercator_tests = read("internal/mercator/mercator_test.go")
    projection_source = read("encoding/mvt/projection.go")
    projection_tests = read("encoding/mvt/projection_test.go")
    for phrase in ["const maxFiniteLevel = 1023", "level > maxFiniteLevel", "scale(level)"]:
        if phrase not in mercator_source:
            failures.append(f"Mercator finite scale boundary must include {phrase}")
    for phrase in ["TestScalarMercatorHighLevels", "TestScalarMercatorExcessiveLevel", "math.MaxUint32"]:
        if phrase not in mercator_tests:
            failures.append(f"Mercator scale tests must include {phrase}")
    if "if extent == 0" not in projection_source or "extent = DefaultExtent" not in projection_source:
        failures.append("MVT projection must default a zero extent before scaling")
    if "math.Ldexp(float64(tile.X), int(n))" not in projection_source or "math.Ldexp(float64(tile.Y), int(n))" not in projection_source:
        failures.append("power-of-two MVT origins must use floating-point scaling")
    for phrase in ["TestPowerOfTwoProjectionHighZoom", "TestProjectionZeroExtentUsesDefault", "math.IsNaN(coordinate)"]:
        if phrase not in projection_tests:
            failures.append(f"MVT projection tests must include {phrase}")

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
        "non-finite interval distances",
        "derived point counts",
        "negative derived point counts",
        "non-finite callback distances",
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
    interval_guidance = [
        read(path).lower() for path in ["README.md", "SECURITY.md", "VISION.md"]
    ]
    if not all("derived point counts" in document for document in interval_guidance):
        failures.append("all guidance must document the derived point-count boundary")
    if not all("negative derived point counts" in document for document in interval_guidance):
        failures.append("all guidance must document the negative point-count boundary")
    if not all("non-finite callback distances" in document for document in interval_guidance):
        failures.append("all guidance must document the non-finite callback boundary")

    for path in ["README.md", "SECURITY.md", "VISION.md"]:
        if "non-finite interval distances" not in read(path).lower():
            failures.append(
                f"{path} must document the non-finite interval distance boundary"
            )

    simplify_exterior_guidance = {
        "README.md": "Polygon simplification drops a polygon when its exterior ring collapses",
        "SECURITY.md": "Simplification must not return polygons whose exterior ring collapses",
        "VISION.md": "Drop polygons whose simplified exterior ring collapses below polygon validity",
        "AGENTS.md": "Polygon simplification must drop a polygon when its exterior ring collapses",
        "CHANGES.md": "collapsed exterior ring",
    }
    for path, phrase in simplify_exterior_guidance.items():
        if phrase not in read(path):
            failures.append(f"{path} must document collapsed polygon simplification")

    simplify_exterior_design = read(SIMPLIFY_COLLAPSED_EXTERIOR_DESIGN)
    for phrase in [
        "## Status: Accepted",
        "Return an empty polygon when its simplified exterior has two or fewer points",
        "MultiPolygon",
    ]:
        if phrase not in simplify_exterior_design:
            failures.append(f"simplify exterior design must record {phrase}")

    simplify_exterior_plan = read(SIMPLIFY_COLLAPSED_EXTERIOR_PLAN)
    for phrase in [
        "## Status: Completed",
        "TestPolygonSkipsCollapsedExteriorRing",
        "RED: Go 1.20.14",
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.11 make check",
        "hostile mutations",
    ]:
        if phrase not in simplify_exterior_plan:
            failures.append(f"simplify exterior plan must record {phrase}")

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
    nonfinite_interval_plan = read(NONFINITE_INTERVAL_PLAN)
    nonfinite_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", nonfinite_interval_plan
    )
    nonfinite_work = markdown_section(nonfinite_interval_plan, "Work Completed")
    nonfinite_verification = markdown_section(
        nonfinite_interval_plan, "Verification Completed"
    )
    if nonfinite_status != ["completed"] or not nonfinite_work:
        failures.append(
            "non-finite interval plan must record one completed status and completed work"
        )
    if not nonfinite_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", nonfinite_verification
    ):
        failures.append(
            "non-finite interval plan must record completed verification"
        )
    for evidence in [
        "GOTOOLCHAIN=go1.20.14 go test ./resample",
        "GOTOOLCHAIN=go1.25.11 go test ./resample",
        "GOTOOLCHAIN=go1.20.14 make check",
        "GOTOOLCHAIN=go1.25.11 make check",
        "from `/tmp`",
        "TestToIntervalRejectsNonFiniteDistance",
    ]:
        if evidence not in nonfinite_verification:
            failures.append(
                f"non-finite interval verification must record {evidence}"
            )
    point_count_plan = read(DERIVED_POINT_COUNT_PLAN)
    point_count_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", point_count_plan
    )
    point_count_work = markdown_section(point_count_plan, "Work Completed")
    point_count_verification = markdown_section(
        point_count_plan, "Verification Completed"
    )
    if (point_count_status != ["completed"] or not point_count_work or
            not point_count_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                point_count_verification,
            )):
        failures.append("derived point-count plan must record completed verification")
    for evidence in [
        "TestToIntervalRejectsUnrepresentablePointCount",
        "Go 1.20.14",
        "Go 1.25.11",
        "make check",
        "external working directory",
        "go mod verify",
        "go build ./...",
        "govulncheck ./...",
        "no vulnerabilities",
        "Six isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in point_count_verification:
            failures.append(f"derived point-count verification must record {evidence}")
    negative_point_plan = read(NEGATIVE_POINT_COUNT_PLAN)
    negative_point_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", negative_point_plan)
    negative_point_work = markdown_section(negative_point_plan, "Work Completed")
    negative_point_verification = markdown_section(negative_point_plan, "Verification Completed")
    if (negative_point_status != ["completed"] or not negative_point_work or
            not negative_point_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                negative_point_verification,
            )):
        failures.append("negative derived point-count plan must record completed verification")
    for evidence in [
        "TestToIntervalRejectsNegativeDerivedPointCount",
        "Go 1.20.14",
        "Go 1.25.11",
        "make check",
        "external working directory",
        "go mod verify",
        "go build ./...",
        "govulncheck ./...",
        "no vulnerabilities",
        "Five isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in negative_point_verification:
            failures.append(f"negative point-count verification must record {evidence}")
    nonfinite_callback_plan = read(NONFINITE_CALLBACK_PLAN)
    nonfinite_callback_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", nonfinite_callback_plan
    )
    nonfinite_callback_work = markdown_section(
        nonfinite_callback_plan, "Work Completed"
    )
    nonfinite_callback_verification = markdown_section(
        nonfinite_callback_plan, "Verification Completed"
    )
    if (nonfinite_callback_status != ["completed"] or not nonfinite_callback_work or
            not nonfinite_callback_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                nonfinite_callback_verification,
            )):
        failures.append("non-finite callback plan must record completed verification")
    for evidence in [
        "TestResampleRejectsNonFiniteCallbackDistance",
        "Go 1.20.14",
        "Go 1.25.11",
        "make check",
        "external working directory",
        "go mod verify",
        "go build ./...",
        "isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in nonfinite_callback_verification:
            failures.append(f"non-finite callback verification must record {evidence}")
    negative_callback_segment_plan = read(NEGATIVE_CALLBACK_SEGMENT_PLAN)
    negative_callback_segment_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", negative_callback_segment_plan
    )
    negative_callback_segment_verification = markdown_section(
        negative_callback_segment_plan, "Verification Completed"
    )
    if (negative_callback_segment_status != ["completed"] or
            "Go 1.20.14" not in negative_callback_segment_verification or
            "Go 1.25.11" not in negative_callback_segment_verification or
            "make check" not in negative_callback_segment_verification or
            "external working directory" not in negative_callback_segment_verification or
            "Six isolated hostile mutations were rejected" not in negative_callback_segment_verification or
            re.search(r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                      negative_callback_segment_verification)):
        failures.append("negative callback segment plan must record completed verification")
    for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        if "negative callback segment distances" not in read(path).lower():
            failures.append(f"{path} must document negative callback segment distances")
    line_string = read("resample/line_string.go")
    line_string_tests = read("resample/line_string_test.go")
    if "spacing := totalDistance / float64(totalPoints-1)" not in line_string or "if !validSpacing(spacing)" not in line_string:
        failures.append("Resample must reject zero or underflowing callback totals before allocation and interpolation")
    for test_name in [
        "TestResampleRejectsZeroCallbackTotal",
        "TestResamplePreservesMixedZeroCallbackSegments",
        "TestResampleDegeneratePublicInputs",
        "TestToIntervalDegeneratePublicInputs",
    ]:
        if f"func {test_name}(" not in line_string_tests:
            failures.append(f"resample regression missing: {test_name}")
    for phrase in [
        "empty Resample input must not call the distance function",
        "single-point Resample input must remain unchanged",
        "zero-length Resample input must not call the distance function",
        "zero-length Resample input must expand to the requested point count",
        "empty ToInterval input must not call the distance function",
        "single-point ToInterval input must remain unchanged",
        "zero-length ToInterval input must collapse to one point",
    ]:
        if phrase not in line_string_tests:
            failures.append(f"resample degenerate fixture missing: {phrase}")
    resample_degenerate_plan = read(RESAMPLE_DEGENERATE_FIXTURES_PLAN)
    resample_degenerate_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", resample_degenerate_plan
    )
    resample_degenerate_verification = markdown_section(
        resample_degenerate_plan, "Verification Completed"
    )
    if (resample_degenerate_status != ["completed"] or
            "Go 1.20.14" not in resample_degenerate_verification or
            "Go 1.25.11" not in resample_degenerate_verification or
            "make check" not in resample_degenerate_verification or
            "go mod verify" not in resample_degenerate_verification or
            "Fourteen isolated hostile mutations were rejected" not in resample_degenerate_verification or
            re.search(r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                      resample_degenerate_verification)):
        failures.append("resample degenerate fixture plan must record completed verification")
    for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        if "empty, single-point, and zero-length resampling" not in read(path).lower():
            failures.append(f"{path} must document degenerate resampling fixtures")
    zero_callback_total_plan = read(ZERO_CALLBACK_TOTAL_PLAN)
    zero_callback_total_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", zero_callback_total_plan
    )
    zero_callback_total_verification = markdown_section(
        zero_callback_total_plan, "Verification Completed"
    )
    if (zero_callback_total_status != ["completed"] or
            "Go 1.20.14" not in zero_callback_total_verification or
            "Go 1.25.11" not in zero_callback_total_verification or
            "make check" not in zero_callback_total_verification or
            "external working directory" not in zero_callback_total_verification or
            "isolated hostile mutations were rejected" not in zero_callback_total_verification or
            re.search(r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                      zero_callback_total_verification)):
        failures.append("zero callback total plan must record completed verification")
    for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        if "zero callback total" not in read(path).lower():
            failures.append(f"{path} must document the zero callback total guard")
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
    if workflow != EXPECTED_CHECK_WORKFLOW:
        failures.append(
            "Check workflow must exactly match the reviewed three-lane execution contract"
        )
    jobs = workflow.split("jobs:\n", 1)[1] if workflow.count("jobs:\n") == 1 else ""
    job_ids = re.findall(r"(?m)^  ([A-Za-z0-9_-]+):\s*$", jobs)
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
        'go-version: ["1.20.14", "1.25.3", "1.25.11"]',
        "GOTOOLCHAIN: local",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")
    if not (
        job_ids == ["test"]
        and workflow.count('go-version: ["1.20.14", "1.25.3", "1.25.11"]') == 1
        and "1.24.0" not in workflow
        and workflow.count("go-version: ${{ matrix.go-version }}") == 1
        and len(re.findall(r"(?m)^      - run: make check\s*$", workflow)) == 1
        and not re.search(r"(?m)^    name:\s*", jobs)
        and not re.search(r"(?m)^        (?:include|exclude):\s*", jobs)
        and "continue-on-error:" not in workflow
        and "needs:" not in workflow
        and "if: always()" not in workflow
    ):
        failures.append(
            "Check workflow must emit three real test matrix lanes that each "
            "run make check without an aggregator or fail-open behavior"
        )

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

    descendant_plan = read(MAPTILE_DESCENDANT_PLAN)
    for phrase in [
        "status: completed",
        "RED: Go 1.20.14",
        "go test ./maptile",
        "MaxZoom",
        "invalid zero-coordinate endpoints",
        "tile-cover merging",
    ]:
        if phrase not in descendant_plan:
            failures.append(f"maptile descendant plan must record {phrase}")

    descendant_guidance = {
        "README.md": "Tiles at `maptile.MaxZoom` have no representable children",
        "SECURITY.md": "Descendant tile operations must not wrap coordinates beyond `maptile.MaxZoom`",
        "VISION.md": "Keep descendant tile operations inside the `maptile.MaxZoom` coordinate ceiling",
        "AGENTS.md": "Tiles at `maptile.MaxZoom` are leaves",
        "CHANGES.md": "canonical invalid zero-coordinate endpoints",
    }
    for path, phrase in descendant_guidance.items():
        if phrase not in read(path):
            failures.append(f"{path} must document the maptile descendant boundary")

    mercator_plan = read(MERCATOR_SCALE_PLAN)
    for phrase in [
        "status: completed",
        "RED: Go 1.20.14",
        "go test ./internal/mercator ./encoding/mvt",
        "level 1023",
        "math.Ldexp",
        "hostile mutations",
    ]:
        if phrase not in mercator_plan:
            failures.append(f"Mercator scale plan must record {phrase}")

    mercator_guidance = {
        "README.md": "Mercator projection preserves finite scales through level 1023",
        "SECURITY.md": "Mercator scale exponents must remain finite",
        "VISION.md": "Keep Mercator scales finite and high-zoom MVT origins free of integer wraparound",
        "CHANGES.md": "power-of-two MVT origins",
    }
    for path, phrase in mercator_guidance.items():
        if phrase not in read(path):
            failures.append(f"{path} must document the Mercator projection scale boundary")

    fraction_plan = read(MAPTILE_FRACTION_PLAN)
    for phrase in ["status: completed", "RED: Go 1.20.14", "TestFraction", "TestExcessiveZoomLineAndPolygonCovers", "hostile mutations"]:
        if phrase not in fraction_plan:
            failures.append(f"maptile fraction plan must record {phrase}")

    fraction_guidance = {
        "README.md": "`maptile.Fraction` follows the same finite exponent boundary",
        "SECURITY.md": "Direct tile fractions must remain finite at excessive zooms",
        "VISION.md": "Keep direct tile fractions finite and unrepresentable tile covers fail-closed",
        "CHANGES.md": "saturated overflowing finite longitude products",
    }
    for path, phrase in fraction_guidance.items():
        if phrase not in read(path):
            failures.append(f"{path} must document the maptile fraction boundary")

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
