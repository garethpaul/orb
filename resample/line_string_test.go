package resample

import (
	"math"
	"math/rand"
	"testing"

	"github.com/paulmach/orb"
	"github.com/paulmach/orb/planar"
)

func TestResampleRejectsNilDistanceFunction(t *testing.T) {
	line := orb.LineString{{0, 0}, {1, 0}}

	if result := Resample(line.Clone(), nil, 2); result != nil {
		t.Fatalf("nil distance function should return nil from Resample: %v", result)
	}
	if result := ToInterval(line.Clone(), nil, 1); result != nil {
		t.Fatalf("nil distance function should return nil from ToInterval: %v", result)
	}
}

func TestResampleRejectsUnboundedPointCount(t *testing.T) {
	line := orb.LineString{{0, 0}, {1, 0}}
	maxInt := int(^uint(0) >> 1)

	if result := Resample(line, planar.Distance, maxInt); result != nil {
		t.Fatalf("unbounded point count should return nil: %d points", len(result))
	}
}

func TestResampleRejectsUnderflowedSpacing(t *testing.T) {
	line := orb.LineString{{0, 0}, {1, 0}}
	tinyDistance := func(orb.Point, orb.Point) float64 {
		return math.SmallestNonzeroFloat64
	}

	if result := Resample(line, tinyDistance, 3); result != nil {
		t.Fatalf("underflowed spacing should return nil, not duplicate samples: %v", result)
	}
}

func TestResampleKeepsFiniteCoordinatesFinite(t *testing.T) {
	line := orb.LineString{{math.MaxFloat64, 0}, {-math.MaxFloat64, 0}}
	unitDistance := func(orb.Point, orb.Point) float64 { return 1 }

	result := Resample(line, unitDistance, 3)
	if len(result) != 3 {
		t.Fatalf("expected three points, got %v", result)
	}
	for i, point := range result {
		if math.IsNaN(point[0]) || math.IsInf(point[0], 0) || math.IsNaN(point[1]) || math.IsInf(point[1], 0) {
			t.Fatalf("point %d is not finite: %v", i, point)
		}
	}
	if result[1] != (orb.Point{0, 0}) {
		t.Fatalf("overflow-safe midpoint incorrect: %v", result[1])
	}
}

func TestResampleStraightLineProperties(t *testing.T) {
	random := rand.New(rand.NewSource(1))
	for iteration := 0; iteration < 250; iteration++ {
		start := random.Float64()*2e6 - 1e6
		end := start + random.Float64()*1e6 + 1
		totalPoints := random.Intn(100) + 2
		line := orb.LineString{{start, 0}, {end, 0}}

		result := Resample(line, planar.Distance, totalPoints)
		if len(result) != totalPoints {
			t.Fatalf("iteration %d: point count %d != %d", iteration, len(result), totalPoints)
		}
		if result[0] != line[0] || result[len(result)-1] != line[1] {
			t.Fatalf("iteration %d: endpoints changed: %v", iteration, result)
		}
		for i := 1; i < len(result); i++ {
			if result[i][0] <= result[i-1][0] || result[i][1] != 0 {
				t.Fatalf("iteration %d: samples do not progress: %v", iteration, result)
			}
		}
	}
}

func TestResample(t *testing.T) {
	ls := orb.LineString{}
	Resample(ls, planar.Distance, 10) // should not panic

	ls = append(ls, orb.Point{0, 0})
	Resample(ls, planar.Distance, 10) // should not panic

	ls = append(ls, orb.Point{1.5, 1.5})
	ls = append(ls, orb.Point{2, 2})

	// resample to 0?
	result := Resample(ls, planar.Distance, 0)
	if len(result) != 0 {
		t.Error("down to zero should be empty line")
	}

	// resample to 1
	result = Resample(ls, planar.Distance, 1)
	answer := orb.LineString{{0, 0}}

	if !result.Equal(answer) {
		t.Error("down to 1 should be first point")
	}

	result = Resample(ls, planar.Distance, 2)
	answer = orb.LineString{{0, 0}, {2, 2}}
	if !result.Equal(answer) {
		t.Error("resample downsampling")
	}

	result = Resample(ls, planar.Distance, 5)
	answer = orb.LineString{{0, 0}, {0.5, 0.5}, {1, 1}, {1.5, 1.5}, {2, 2}}
	if !result.Equal(answer) {
		t.Error("resample upsampling")
		t.Log(result)
		t.Log(answer)
	}

	// round off error case, triggered on my laptop
	p1 := orb.LineString{{-88.145243, 42.321059}, {-88.145232, 42.325902}}
	p1 = Resample(p1, planar.Distance, 109)
	if len(p1) != 109 {
		t.Errorf("incorrect length: %v != 109", len(p1))
	}

	// duplicate points
	ls = orb.LineString{{1, 0}, {1, 0}, {1, 0}}
	ls = Resample(ls, planar.Distance, 10)
	if l := len(ls); l != 10 {
		t.Errorf("length incorrect: %d != 10", l)
	}

	expected := orb.Point{1, 0}
	for i := 0; i < len(ls); i++ {
		if !ls[i].Equal(expected) {
			t.Errorf("incorrect point: %v != %v", ls[i], expected)
		}
	}
}

func TestToInterval(t *testing.T) {
	ls := orb.LineString{{0, 0}, {0, 1}, {0, 10}}

	cases := []struct {
		name     string
		distance float64
		line     orb.LineString
		expected orb.LineString
	}{
		{
			name:     "same number of points",
			distance: 5.0,
			expected: orb.LineString{{0, 0}, {0, 5}, {0, 10}},
		},
		{
			name:     "dist less than 0",
			distance: -5.0,
			expected: nil,
		},
		{
			name:     "dist less than 0",
			distance: -5.0,
			expected: nil,
		},
		{
			name:     "return same if short line",
			distance: 5.0,
			line:     orb.LineString{{0, 0}},
			expected: orb.LineString{{0, 0}},
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			in := ls.Clone()
			if tc.line != nil {
				in = tc.line
			}

			ls := ToInterval(in, planar.Distance, tc.distance)
			if !ls.Equal(tc.expected) {
				t.Errorf("incorrect point: %v != %v", ls, tc.expected)
			}
		})
	}
}

func TestToIntervalEmptyLineString(t *testing.T) {
	distanceCalled := false
	distance := func(a, b orb.Point) float64 {
		distanceCalled = true
		return planar.Distance(a, b)
	}

	if result := ToInterval(nil, distance, 5); result != nil {
		t.Fatalf("nil line string should remain nil: %v", result)
	}

	empty := orb.LineString{}
	result := ToInterval(empty, distance, 5)
	if result == nil || len(result) != 0 {
		t.Fatalf("empty line string should remain non-nil and empty: %v", result)
	}

	single := orb.LineString{{1, 2}}
	if result := ToInterval(single, distance, 5); !result.Equal(single) {
		t.Fatalf("single-point line string should remain unchanged: %v", result)
	}
	if distanceCalled {
		t.Fatal("distance function should not be called for short line strings")
	}
}

func TestToIntervalRejectsNonFiniteDistance(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 10}}

	for _, tc := range []struct {
		name     string
		distance float64
	}{
		{name: "NaN", distance: math.NaN()},
		{name: "positive infinity", distance: math.Inf(1)},
		{name: "negative infinity", distance: math.Inf(-1)},
	} {
		t.Run(tc.name, func(t *testing.T) {
			distanceCalled := false
			distance := func(a, b orb.Point) float64 {
				distanceCalled = true
				return planar.Distance(a, b)
			}

			if result := ToInterval(line, distance, tc.distance); result != nil {
				t.Fatalf("non-finite interval should return nil: %v", result)
			}
			if result := ToInterval(orb.LineString{{0, 0}}, distance, tc.distance); result != nil {
				t.Fatalf("non-finite interval should be rejected before short-line handling: %v", result)
			}
			if distanceCalled {
				t.Fatal("distance function should not be called for non-finite intervals")
			}
		})
	}
}

func TestToIntervalRejectsUnrepresentablePointCount(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 10}}
	result := ToInterval(line, planar.Distance, math.SmallestNonzeroFloat64)
	if result != nil {
		t.Fatalf("unrepresentable point count should return nil: %v", result)
	}
}

func TestToIntervalRejectsNegativeDerivedPointCount(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 10}}
	negativeDistance := func(a, b orb.Point) float64 {
		return -planar.Distance(a, b)
	}

	if result := ToInterval(line, negativeDistance, 1); result != nil {
		t.Fatalf("negative derived point count should return nil: %v", result)
	}
}

func TestResampleRejectsNonFiniteCallbackDistance(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 5}, {0, 10}}

	for _, tc := range []struct {
		name     string
		distance float64
	}{
		{name: "NaN", distance: math.NaN()},
		{name: "positive infinity", distance: math.Inf(1)},
		{name: "negative infinity", distance: math.Inf(-1)},
		{name: "finite cumulative overflow", distance: math.MaxFloat64},
	} {
		t.Run(tc.name, func(t *testing.T) {
			distance := func(orb.Point, orb.Point) float64 {
				return tc.distance
			}

			if result := Resample(line.Clone(), distance, 3); result != nil {
				t.Fatalf("non-finite callback distance should return nil from Resample: %v", result)
			}
			if result := ToInterval(line.Clone(), distance, 1); result != nil {
				t.Fatalf("non-finite callback distance should return nil from ToInterval: %v", result)
			}
		})
	}
}

func TestResampleRejectsNegativeCallbackSegmentDistance(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 5}, {0, 10}}

	negativeThenPositive := func() orb.DistanceFunc {
		calls := 0
		return func(orb.Point, orb.Point) float64 {
			calls++
			if calls == 1 {
				return -1
			}
			return 11
		}
	}

	if result := Resample(line.Clone(), negativeThenPositive(), 3); result != nil {
		t.Fatalf("negative callback segment should return nil from Resample: %v", result)
	}
	if result := ToInterval(line.Clone(), negativeThenPositive(), 1); result != nil {
		t.Fatalf("negative callback segment should return nil from ToInterval: %v", result)
	}
}

func TestResampleRejectsZeroCallbackTotal(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 5}, {0, 10}}
	zeroDistance := func(orb.Point, orb.Point) float64 { return 0 }

	if result := Resample(line.Clone(), zeroDistance, 3); result != nil {
		t.Fatalf("zero callback total should return nil from Resample: %v", result)
	}
	if result := ToInterval(line.Clone(), zeroDistance, 1); result != nil {
		t.Fatalf("zero callback total should return nil from ToInterval: %v", result)
	}
}

func TestResamplePreservesMixedZeroCallbackSegments(t *testing.T) {
	line := orb.LineString{{0, 0}, {0, 5}, {0, 10}}
	calls := 0
	mixedDistance := func(orb.Point, orb.Point) float64 {
		calls++
		if calls == 1 {
			return 0
		}
		return 10
	}

	expected := orb.LineString{{0, 0}, {0, 7.5}, {0, 10}}
	if result := Resample(line.Clone(), mixedDistance, 3); !result.Equal(expected) {
		t.Fatalf("mixed zero callback segments should remain supported: %v != %v", result, expected)
	}
}

func TestLineStringResampleEdgeCases(t *testing.T) {
	ls := orb.LineString{{0, 0}}

	_, ret := resampleEdgeCases(ls, 10)
	if !ret {
		t.Errorf("should return true")
	}

	// duplicate points
	ls = append(ls, orb.Point{0, 0})
	ls, ret = resampleEdgeCases(ls, 10)
	if !ret {
		t.Errorf("should return true")
	}

	if l := len(ls); l != 10 {
		t.Errorf("should reset to suggested points: %v != 10", l)
	}

	ls, _ = resampleEdgeCases(ls, 5)
	if l := len(ls); l != 5 {
		t.Errorf("should shorten if necessary: %v != 5", l)
	}
}
