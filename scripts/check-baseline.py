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

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in [
        "make check",
        "go test ./...",
        "go vet ./...",
        "github.com/paulmach/orb",
        "Go module",
        "Mapbox Vector Tile",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "go test ./..." not in plan or "go vet ./..." not in plan:
        failures.append("plan must record completed status and Go verification")

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
