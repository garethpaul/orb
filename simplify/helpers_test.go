package simplify

import (
	"testing"

	"github.com/paulmach/orb"
)

func TestSimplify(t *testing.T) {
	r := DouglasPeucker(10)
	for _, g := range orb.AllGeometries {
		simplify(r, g)
	}
}

func TestPolygon(t *testing.T) {
	p := orb.Polygon{
		{{0, 0}, {1, 0}, {1, 1}, {0, 0}},
		{{0, 0}, {0, 0}},
	}

	p = DouglasPeucker(0).Polygon(p)
	if len(p) != 1 {
		t.Errorf("should remove empty ring")
	}
}

func TestPolygonSkipsCollapsedExteriorRing(t *testing.T) {
	p := orb.Polygon{
		{{0, 0}, {2, 0}, {2, 2}, {0, 2}, {0, 0}},
	}

	p = DouglasPeucker(100).Polygon(p)
	if len(p) != 0 {
		t.Fatalf("should drop polygon with collapsed exterior ring: %v", p)
	}
}

func TestPolygonDoesNotPromoteInteriorRing(t *testing.T) {
	p := orb.Polygon{
		{{0, 0}, {0, 0}, {0, 0}},
		{{1, 1}, {3, 1}, {3, 3}, {1, 3}, {1, 1}},
	}

	p = DouglasPeucker(0).Polygon(p)
	if len(p) != 0 {
		t.Fatalf("should not promote an interior ring after exterior collapse: %v", p)
	}
}

func TestMultiPolygon(t *testing.T) {
	mp := orb.MultiPolygon{
		{{{0, 0}, {1, 0}, {1, 1}, {0, 0}}},
		{{{0, 0}, {0, 0}}},
	}

	mp = DouglasPeucker(0).MultiPolygon(mp)
	if len(mp) != 1 {
		t.Errorf("should remove empty polygon")
	}
}

func TestMultiPolygonSkipsEmptyPolygon(t *testing.T) {
	mp := orb.MultiPolygon{
		{},
		{{{0, 0}, {1, 0}, {1, 1}, {0, 0}}},
	}

	mp = DouglasPeucker(0).MultiPolygon(mp)
	if len(mp) != 1 {
		t.Errorf("should skip empty polygon without panicking")
	}
}
