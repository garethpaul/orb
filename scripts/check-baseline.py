#!/usr/bin/env python3
"""Static baseline checks for the orb Go geometry library."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-orb-go-module-baseline.md"
REQUIRED = [
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
    for phrase in ["go test ./...", "go vet ./...", "python3 scripts/check-baseline.py", "check: test vet static-check"]:
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
    if "if b.IsEmpty()" not in bound or "return other" not in bound:
        failures.append("Bound.Union must return the other bound when the receiver is empty")
    if "TestBoundUnionWithEmptyReceiver" not in bound_tests:
        failures.append("bound tests must cover empty receiver union")
    if "TestMultiLineString_BoundSkipsLeadingEmptyLineString" not in multi_line_tests:
        failures.append("multi line string tests must cover leading empty bounds")

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in [
        "make check",
        "go test ./...",
        "go vet ./...",
        "github.com/paulmach/orb",
        "Go module",
        "Mapbox Vector Tile",
        "degenerate rings",
        "empty line strings",
        "nil geometries",
        "empty bounds",
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
