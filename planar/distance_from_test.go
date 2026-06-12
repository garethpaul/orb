package planar

import (
	"math"
	"testing"

	"github.com/paulmach/orb"
)

var epsilon = 1e-6

func TestDistanceFromSegment(t *testing.T) {
	a := orb.Point{0, 0}
	b := orb.Point{0, 10}

	cases := []struct {
		name   string
		point  orb.Point
		result float64
	}{
		{
			name:   "point in middle",
			point:  orb.Point{1, 5},
			result: 1,
		},
		{
			name:   "on line",
			point:  orb.Point{0, 2},
			result: 0,
		},
		{
			name:   "past start",
			point:  orb.Point{0, -5},
			result: 5,
		},
		{
			name:   "past end",
			point:  orb.Point{0, 13},
			result: 3,
		},
		{
			name:   "triangle",
			point:  orb.Point{3, 4},
			result: 3,
		},
		{
			name:   "triangle off end",
			point:  orb.Point{3, -4},
			result: 5,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			v := DistanceFromSegment(a, b, tc.point)
			if v != tc.result {
				t.Errorf("incorrect distance: %v != %v", v, tc.result)
			}
		})
	}
}

func TestDistanceFromWithIndex(t *testing.T) {
	for _, g := range orb.AllGeometries {
		DistanceFromWithIndex(g, orb.Point{})
	}
}

func TestDistanceFrom_MultiPoint(t *testing.T) {
	mp := orb.MultiPoint{{0.0}, {1, 1}, {2, 2}}

	fromPoint := orb.Point{3, 2}
	if distance := DistanceFrom(mp, fromPoint); distance != 1 {
		t.Errorf("distance incorrect: %v != %v", distance, 1)
	}
}

func TestDistanceFrom_LineString(t *testing.T) {
	ls := orb.LineString{{0, 0}, {0, 3}, {4, 3}, {4, 0}}

	cases := []struct {
		name   string
		point  orb.Point
		result float64
	}{
		{
			point:  orb.Point{4.5, 1.5},
			result: 0.5,
		},
		{
			point:  orb.Point{0.4, 1.5},
			result: 0.4,
		},
		{
			point:  orb.Point{-0.3, 1.5},
			result: 0.3,
		},
		{
			point:  orb.Point{0.3, 2.8},
			result: 0.2,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			d := DistanceFrom(ls, tc.point)
			if math.Abs(d-tc.result) > epsilon {
				t.Errorf("incorrect distance: %v != %v", d, tc.result)
			}
		})
	}
}

func TestDistanceFrom_Polygon(t *testing.T) {
	r1 := orb.Ring{{0, 0}, {3, 0}, {3, 3}, {0, 3}, {0, 0}}
	r2 := orb.Ring{{1, 1}, {2, 1}, {2, 2}, {1, 2}, {1, 1}}
	poly := orb.Polygon{r1, r2}

	cases := []struct {
		name   string
		point  orb.Point
		result float64
	}{
		{
			name:   "outside",
			point:  orb.Point{-1, 2},
			result: 1,
		},
		{
			name:   "inside",
			point:  orb.Point{0.4, 2},
			result: 0.4,
		},
		{
			name:   "in hole",
			point:  orb.Point{1.3, 1.4},
			result: 0.3,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if d := DistanceFrom(poly, tc.point); math.Abs(d-tc.result) > epsilon {
				t.Errorf("incorrect distance: %v != %v", d, tc.result)
			}
		})
	}
}

func TestDistanceFromWithIndex_PolygonReturnsRingIndex(t *testing.T) {
	outer := orb.Ring{{0, 0}, {3, 0}, {3, 3}, {0, 3}, {0, 0}}
	hole := orb.Ring{{1, 1}, {2, 1}, {2, 2}, {1, 2}, {1, 1}}
	polygon := orb.Polygon{outer, hole}

	tests := []struct {
		name     string
		point    orb.Point
		distance float64
		index    int
	}{
		{
			name:     "outer ring nearest on nonzero segment",
			point:    orb.Point{-1, 2},
			distance: 1,
			index:    0,
		},
		{
			name:     "hole ring nearest on different segment",
			point:    orb.Point{1.5, 1.8},
			distance: 0.2,
			index:    1,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			distance, index := DistanceFromWithIndex(polygon, test.point)
			if math.Abs(distance-test.distance) > epsilon {
				t.Fatalf("incorrect distance: %v != %v", distance, test.distance)
			}
			if index != test.index {
				t.Fatalf("incorrect ring index: %d != %d", index, test.index)
			}
		})
	}
}

func TestDistanceFromWithIndex_EmptyPolygon(t *testing.T) {
	distance, index := DistanceFromWithIndex(orb.Polygon{}, orb.Point{})
	if !math.IsInf(distance, 1) || index != -1 {
		t.Fatalf("empty polygon result: (%v, %d) != (+Inf, -1)", distance, index)
	}
}
