package orb

import (
	"fmt"
	"reflect"
	"testing"
)

func TestRound(t *testing.T) {
	for _, g := range AllGeometries {
		// this closure is necessary if tests are run in parallel, maybe
		func(geom Geometry) {
			t.Run(fmt.Sprintf("%T", g), func(t *testing.T) {
				// should not panic
				Round(geom)
			})
		}(g)
	}

	cases := []struct {
		name   string
		input  Point
		factor int
		result Point
	}{
		{
			name:   "round out",
			input:  Point{0.007, -0.007},
			factor: 1e2,
			result: Point{0.01, -0.01},
		},
		{
			name:   "round in",
			input:  Point{0.12345, -0.12345},
			factor: 1e3,
			result: Point{0.123, -0.123},
		},
		{
			name:   "round out on tie",
			input:  Point{0.15, -0.15},
			factor: 1e1,
			result: Point{0.2, -0.2},
		},
	}

	for _, tc := range cases {
		t.Run(tc.name+" - point", func(t *testing.T) {
			r := Round(tc.input, tc.factor).(Point)
			if !r.Equal(tc.result) {
				t.Errorf("point round incorrect: %v != %v", r, tc.result)
			}
		})

		t.Run(tc.name+" - list", func(t *testing.T) {
			r := Round(LineString{tc.input}, tc.factor).(LineString)
			if !r[0].Equal(tc.result) {
				t.Errorf("list round incorrect: %v != %v", r[0], tc.result)
			}
		})

		t.Run(tc.name+" - bound", func(t *testing.T) {
			r := Round(Bound{Min: tc.input, Max: tc.input}, tc.factor).(Bound)
			if !r.Min.Equal(tc.result) {
				t.Errorf("bound min incorrect: %v != %v", r.Min, tc.result)
			}

			if !r.Max.Equal(tc.result) {
				t.Errorf("bound max incorrect: %v != %v", r.Max, tc.result)
			}
		})
	}

	t.Run("default to 6 decimal places", func(t *testing.T) {
		r := Round(Point{0.123456789, -0.123456789}).(Point)
		if !r.Equal(Point{0.123457, -0.123457}) {
			t.Errorf("incorrect default round: %v", r)
		}
	})

	t.Run("collection preserves nil child", func(t *testing.T) {
		result := Round(Collection{nil, Point{0.15, -0.15}}, 10)
		expected := Collection{nil, Point{0.2, -0.2}}
		if !reflect.DeepEqual(result, expected) {
			t.Fatalf("collection round = %#v, want %#v", result, expected)
		}
	})
}

func TestRoundZeroFactorLeavesGeometryUnchanged(t *testing.T) {
	input := Collection{
		nil,
		Point{0.123456789, -0.123456789},
		LineString{{1.23456789, -1.23456789}},
		Bound{
			Min: Point{-2.3456789, -3.456789},
			Max: Point{2.3456789, 3.456789},
		},
	}
	expected := Collection{
		nil,
		Point{0.123456789, -0.123456789},
		LineString{{1.23456789, -1.23456789}},
		Bound{
			Min: Point{-2.3456789, -3.456789},
			Max: Point{2.3456789, 3.456789},
		},
	}

	result := Round(input, 0)
	if !reflect.DeepEqual(result, expected) {
		t.Fatalf("Round(%v, 0) = %#v, want unchanged %#v", input, result, expected)
	}
}

func TestRoundNegativeFactorMatchesPositiveFactor(t *testing.T) {
	negativeInput := Collection{nil, Point{0.12345, -0.12345}}
	positiveInput := Collection{nil, Point{0.12345, -0.12345}}

	result := Round(negativeInput, -1000)
	expected := Round(positiveInput, 1000)
	if !reflect.DeepEqual(result, expected) {
		t.Fatalf("negative factor result = %#v, want positive-factor result %#v", result, expected)
	}
}
