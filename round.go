package orb

import (
	"fmt"
	"math"
)

// Round will round all the coordinates of the geometry to the given factor.
// The default is 6 decimal places. A zero factor leaves the geometry unchanged.
func Round(g Geometry, factor ...int) Geometry {
	if g == nil {
		return nil
	}

	f := DefaultRoundingFactor
	if len(factor) > 0 {
		f = float64(factor[0])
	}
	if f == 0 {
		return g
	}

	return round(g, f)
}

func round(g Geometry, f float64) Geometry {
	if g == nil {
		return nil
	}

	switch g := g.(type) {
	case Point:
		return Point{
			math.Round(g[0]*f) / f,
			math.Round(g[1]*f) / f,
		}
	case MultiPoint:
		if g == nil {
			return nil
		}
		roundPoints([]Point(g), f)
		return g
	case LineString:
		if g == nil {
			return nil
		}
		roundPoints([]Point(g), f)
		return g
	case MultiLineString:
		if g == nil {
			return nil
		}
		for _, ls := range g {
			roundPoints([]Point(ls), f)
		}
		return g
	case Ring:
		if g == nil {
			return nil
		}
		roundPoints([]Point(g), f)
		return g
	case Polygon:
		if g == nil {
			return nil
		}
		for _, r := range g {
			roundPoints([]Point(r), f)
		}
		return g
	case MultiPolygon:
		if g == nil {
			return nil
		}
		for _, p := range g {
			for _, r := range p {
				roundPoints([]Point(r), f)
			}
		}
		return g
	case Collection:
		if g == nil {
			return nil
		}

		for i := range g {
			g[i] = round(g[i], f)
		}
		return g
	case Bound:
		return Bound{
			Min: Point{
				math.Round(g.Min[0]*f) / f,
				math.Round(g.Min[1]*f) / f,
			},
			Max: Point{
				math.Round(g.Max[0]*f) / f,
				math.Round(g.Max[1]*f) / f,
			},
		}
	}

	panic(fmt.Sprintf("geometry type not supported: %T", g))
}

func roundPoints(ps []Point, f float64) {
	for i := range ps {
		ps[i][0] = math.Round(ps[i][0]*f) / f
		ps[i][1] = math.Round(ps[i][1]*f) / f
	}
}
