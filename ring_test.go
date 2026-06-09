package orb

import (
	"testing"
)

func TestRing_Closed(t *testing.T) {
	cases := []struct {
		name   string
		ring   Ring
		closed bool
	}{
		{
			name:   "empty ring is not closed",
			ring:   Ring{},
			closed: false,
		},
		{
			name:   "one point ring is not closed",
			ring:   Ring{{3, 0}},
			closed: false,
		},
		{
			name:   "first must equal last",
			ring:   Ring{{0, 0}, {3, 0}, {3, 4}, {0, 0}},
			closed: true,
		},
		{
			name:   "not closed if last point does not match",
			ring:   Ring{{0, 0}, {3, 0}, {3, 4}},
			closed: false,
		},
		{
			name:   "too-short ring is not closed even when endpoints match",
			ring:   Ring{{3, 0}, {3, 0}},
			closed: false,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if v := tc.ring.Closed(); v != tc.closed {
				t.Errorf("incorrect: %v != %v", v, tc.closed)
			}
		})
	}
}

func TestRing_OrientationDegenerate(t *testing.T) {
	cases := []struct {
		name string
		ring Ring
	}{
		{
			name: "empty ring",
			ring: Ring{},
		},
		{
			name: "one point ring",
			ring: Ring{{0, 0}},
		},
		{
			name: "two point ring",
			ring: Ring{{0, 0}, {1, 1}},
		},
		{
			name: "collinear ring",
			ring: Ring{{0, 0}, {1, 1}, {2, 2}},
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if val := tc.ring.Orientation(); val != 0 {
				t.Errorf("degenerate ring should have zero orientation: %v", val)
			}
		})
	}
}

func TestRing_Orientation(t *testing.T) {
	cases := []struct {
		name   string
		ring   Ring
		result Orientation
	}{
		{
			name:   "simple box, ccw",
			ring:   Ring{{0, 0}, {0.001, 0}, {0.001, 0.001}, {0, 0.001}, {0, 0}},
			result: CCW,
		},
		{
			name:   "simple box, cw",
			ring:   Ring{{0, 0}, {0, 0.001}, {0.001, 0.001}, {0.001, 0}, {0, 0}},
			result: CW,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			val := tc.ring.Orientation()
			if val != tc.result {
				t.Errorf("wrong orientation: %v != %v", val, tc.result)
			}

			// should work without redudant last point.
			ring := tc.ring[:len(tc.ring)-1]
			val = ring.Orientation()
			if val != tc.result {
				t.Errorf("wrong orientation: %v != %v", val, tc.result)
			}
		})
	}
}
