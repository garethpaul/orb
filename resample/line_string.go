// Package resample has a couple functions for resampling line geometry
// into more or less evenly spaces points.
package resample

import (
	"math"

	"github.com/paulmach/orb"
)

const (
	maxResampleAllocationBytes = 64 << 20
	bytesPerPoint              = 2 * 8
	maxResamplePoints          = maxResampleAllocationBytes / bytesPerPoint
)

// Resample converts the line string into totalPoints-1 evenly spaced segments.
// This function will modify the linestring input.
func Resample(ls orb.LineString, df orb.DistanceFunc, totalPoints int) orb.LineString {
	if totalPoints <= 0 || totalPoints > maxResamplePoints || !finiteLineString(ls) {
		return nil
	}

	ls, ret := resampleEdgeCases(ls, totalPoints)
	if ret {
		return ls
	}
	// precomputes the total distance and intermediate distances
	total, dists, ok := precomputeDistances(ls, df)
	if !ok {
		return nil
	}
	return resample(ls, dists, total, totalPoints)
}

// ToInterval coverts the line string into evenly spaced points of
// about the given distance.
// This function will modify the linestring input.
func ToInterval(ls orb.LineString, df orb.DistanceFunc, dist float64) orb.LineString {
	if !validSpacing(dist) || !finiteLineString(ls) {
		return nil
	}
	if len(ls) <= 1 {
		return ls
	}
	// precomputes the total distance and intermediate distances
	total, dists, ok := precomputeDistances(ls, df)
	if !ok {
		return nil
	}
	if total == 0 {
		if allPointsEqual(ls) {
			return ls[:1]
		}
		return nil
	}

	pointCount := total / dist
	if pointCount < 0 || math.IsNaN(pointCount) || math.IsInf(pointCount, 0) || pointCount >= float64(maxResamplePoints) {
		return nil
	}
	totalPoints := int(pointCount) + 1
	ls, ret := resampleEdgeCases(ls, totalPoints)
	if ret {
		return ls
	}

	return resample(ls, dists, total, totalPoints)
}

func resample(ls orb.LineString, dists []float64, totalDistance float64, totalPoints int) orb.LineString {
	if totalPoints == 1 {
		return ls[:1]
	}

	spacing := totalDistance / float64(totalPoints-1)
	if !validSpacing(spacing) {
		return nil
	}

	points := make([]orb.Point, 1, totalPoints)
	points[0] = ls[0] // start stays the same

	step := 1
	dist := 0.0

	currentDistance := spacing
	// declare here and update had nice performance benefits need to retest
	currentSeg := [2]orb.Point{}
	for i := 0; i < len(ls)-1; i++ {
		currentSeg[0] = ls[i]
		currentSeg[1] = ls[i+1]

		currentSegDistance := dists[i]
		nextDistance := dist + currentSegDistance
		if currentSegDistance == 0 {
			dist = nextDistance
			continue
		}

		for step < totalPoints && currentDistance <= nextDistance {
			// need to add a point
			percent := (currentDistance - dist) / currentSegDistance
			if math.IsNaN(percent) || math.IsInf(percent, 0) || percent < 0 || percent > 1 {
				return nil
			}
			point := orb.Point{
				interpolate(currentSeg[0][0], currentSeg[1][0], percent),
				interpolate(currentSeg[0][1], currentSeg[1][1], percent),
			}
			if !finitePoint(point) {
				return nil
			}
			points = append(points, point)

			// move to the next distance we want
			step++
			currentDistance = totalDistance * float64(step) / float64(totalPoints-1)
			if step == totalPoints-1 { // weird round off error on my machine
				currentDistance = totalDistance
			}
		}

		// past the current point in the original segment, so move to the next one
		dist = nextDistance
	}
	if len(points) != totalPoints {
		return nil
	}

	// end stays the same, to handle round off errors
	points[totalPoints-1] = ls[len(ls)-1]

	return orb.LineString(points)
}

// resampleEdgeCases is used to handle edge case for
// resampling like not enough points and the line string is all the same point.
// will return nil if there are no edge cases. If return true if
// one of these edge cases was found and handled.
func resampleEdgeCases(ls orb.LineString, totalPoints int) (orb.LineString, bool) {
	// degenerate case
	if len(ls) <= 1 {
		return ls, true
	}
	if totalPoints == 1 {
		return ls[:1], true
	}

	// if all the points are the same, treat as special case.
	if allPointsEqual(ls) {
		if totalPoints > len(ls) {
			// extend to be requested length
			for len(ls) != totalPoints {
				ls = append(ls, ls[0])
			}

			return ls, true
		}

		// contract to be requested length
		ls = ls[:totalPoints]
		return ls, true
	}

	return ls, false
}

func allPointsEqual(ls orb.LineString) bool {
	for _, point := range ls[1:] {
		if !ls[0].Equal(point) {
			return false
		}
	}
	return true
}

// precomputeDistances precomputes the total distance and intermediate distances.
func precomputeDistances(ls orb.LineString, df orb.DistanceFunc) (float64, []float64, bool) {
	if df == nil {
		return 0, nil, false
	}

	total := 0.0
	dists := make([]float64, len(ls)-1)
	for i := 0; i < len(ls)-1; i++ {
		dists[i] = df(ls[i], ls[i+1])
		if dists[i] < 0 || math.IsNaN(dists[i]) || math.IsInf(dists[i], 0) {
			return 0, nil, false
		}
		total += dists[i]
		if math.IsNaN(total) || math.IsInf(total, 0) {
			return 0, nil, false
		}
	}

	return total, dists, true
}

func validSpacing(value float64) bool {
	return value > 0 && !math.IsNaN(value) && !math.IsInf(value, 0)
}

func finiteLineString(ls orb.LineString) bool {
	for _, point := range ls {
		if !finitePoint(point) {
			return false
		}
	}
	return true
}

func finitePoint(point orb.Point) bool {
	return !math.IsNaN(point[0]) && !math.IsInf(point[0], 0) &&
		!math.IsNaN(point[1]) && !math.IsInf(point[1], 0)
}

func interpolate(a, b, percent float64) float64 {
	return (1-percent)*a + percent*b
}
