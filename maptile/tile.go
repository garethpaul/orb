// Package maptile defines a Tile type and methods to work with
// web map projected tile data.
package maptile

import (
	"math"
	"math/bits"

	"github.com/paulmach/orb"
	"github.com/paulmach/orb/geojson"
	"github.com/paulmach/orb/internal/mercator"
)

// Tiles is a set of tiles, later we can add methods to this.
type Tiles []Tile

// ToFeatureCollection converts the tiles into a feature collection.
// This method is mostly useful for debugging output.
func (ts Tiles) ToFeatureCollection() *geojson.FeatureCollection {
	fc := geojson.NewFeatureCollection()
	fc.Features = make([]*geojson.Feature, 0, len(ts))
	for _, t := range ts {
		fc.Append(geojson.NewFeature(t.Bound().ToPolygon()))
	}

	return fc
}

// Tile is an x, y, z web mercator tile.
type Tile struct {
	X, Y uint32
	Z    Zoom
}

// A Zoom is a strict type for a tile zoom level.
type Zoom uint32

// MaxZoom is the highest zoom whose complete tile coordinate range fits in uint32.
const MaxZoom Zoom = 32

const maxFiniteZoom Zoom = 1023

// New creates a new tile with the given coordinates.
func New(x, y uint32, z Zoom) Tile {
	return Tile{x, y, z}
}

// At creates a tile for the point at the given zoom.
// Will create a valid tile through MaxZoom. Higher zooms return an invalid tile.
// Points outside longitude [-180, 180] or latitude [-85.0511, 85.0511]
// will be snapped to the max or min tile as appropriate.
func At(ll orb.Point, z Zoom) Tile {
	if z > MaxZoom {
		return Tile{Z: z}
	}

	f := Fraction(ll, z)
	maxCoordinate := math.Exp2(float64(z)) - 1
	t := Tile{
		X: boundedCoordinate(f[0], maxCoordinate),
		Y: boundedCoordinate(f[1], maxCoordinate),
		Z: z,
	}

	return t
}

func boundedCoordinate(value, max float64) uint32 {
	if math.IsNaN(value) || value < 0 {
		return 0
	}
	if value > max {
		return uint32(max)
	}

	return uint32(value)
}

// FromQuadkey creates the tile from the quadkey.
func FromQuadkey(k uint64, z Zoom) Tile {
	t := Tile{Z: z}

	for i := Zoom(0); i < z; i++ {
		t.X |= uint32((k & (1 << (2 * i))) >> i)
		t.Y |= uint32((k & (1 << (2*i + 1))) >> (i + 1))
	}

	return t
}

// Valid returns if the tile's x/y are within the range for the tile's zoom.
func (t Tile) Valid() bool {
	if t.Z > MaxZoom {
		return false
	}
	if t.Z == MaxZoom {
		return true
	}

	maxIndex := uint32(1) << uint32(t.Z)
	return t.X < maxIndex && t.Y < maxIndex
}

// Bound returns the geo bound for the tile.
// An optional tileBuffer parameter can be passes to create a buffer
// around the bound in tile dimension. e.g. a tileBuffer of 1 would create
// a bound 9x the size of the tile, centered around the provided tile.
func (t Tile) Bound(tileBuffer ...float64) orb.Bound {
	buffer := 0.0
	if len(tileBuffer) > 0 {
		buffer = tileBuffer[0]
	}

	x := float64(t.X)
	y := float64(t.Y)

	minx := x - buffer

	miny := y - buffer
	if miny < 0 {
		miny = 0
	}

	lon1, lat1 := mercator.ToGeo(minx, miny, uint32(t.Z))

	maxx := x + 1 + buffer

	maxtiles := math.Exp2(float64(t.Z))
	maxy := y + 1 + buffer
	if maxy > maxtiles {
		maxy = maxtiles
	}

	lon2, lat2 := mercator.ToGeo(maxx, maxy, uint32(t.Z))

	return orb.Bound{
		Min: orb.Point{lon1, lat2},
		Max: orb.Point{lon2, lat1},
	}
}

// Center returns the center of the tile.
func (t Tile) Center() orb.Point {
	return t.Bound(0).Center()
}

// Contains returns if the given tile is fully contained (or equal to) the give tile.
func (t Tile) Contains(tile Tile) bool {
	if tile.Z < t.Z {
		return false
	}

	return t == tile.toZoom(t.Z)
}

// Parent returns the parent of the tile.
func (t Tile) Parent() Tile {
	if t.Z == 0 {
		return t
	}

	return Tile{
		X: t.X >> 1,
		Y: t.Y >> 1,
		Z: t.Z - 1,
	}
}

// Fraction returns the precise tile fraction at the given zoom.
// Zooms above 1023 use 1023 as the effective zoom.
// Will return 2^effectiveZoom-1 if the point is below 85.0511 S.
func Fraction(ll orb.Point, z Zoom) orb.Point {
	var p orb.Point

	if z > maxFiniteZoom {
		z = maxFiniteZoom
	}
	maxtiles := math.Exp2(float64(z))

	lng := ll[0]/360.0 + 0.5
	p[0] = finiteProduct(lng, maxtiles)

	// bound it because we have a top of the world problem
	if ll[1] < -85.0511 {
		p[1] = maxtiles - 1
	} else if ll[1] > 85.0511 {
		p[1] = 0
	} else {
		siny := math.Sin(ll[1] * math.Pi / 180.0)
		lat := 0.5 + 0.5*math.Log((1.0+siny)/(1.0-siny))/(-2*math.Pi)
		p[1] = lat * maxtiles
	}

	return p
}

func finiteProduct(value, scale float64) float64 {
	product := value * scale
	if math.IsInf(product, 0) {
		return math.Copysign(math.MaxFloat64, product)
	}

	return product
}

// SharedParent returns the tile that contains both the tiles.
func (t Tile) SharedParent(tile Tile) Tile {
	// bring both tiles to the lowest zoom.
	if t.Z != tile.Z {
		if t.Z < tile.Z {
			tile = tile.toZoom(t.Z)
		} else {
			t = t.toZoom(tile.Z)
		}
	}

	if t == tile {
		return t
	}

	// go version < 1.9
	// bit package usage was about 10% faster
	//
	// TODO: use build flags to support older versions of go.
	//
	// move from most significant to least until there isn't a match.
	// for i := t.Z - 1; i >= 0; i-- {
	// 	if t.X&(1<<i) != tile.X&(1<<i) ||
	// 		t.Y&(1<<i) != tile.Y&(1<<i) {
	// 		return Tile{
	// 			t.X >> (i + 1),
	// 			t.Y >> (i + 1),
	// 			t.Z - (i + 1),
	// 		}
	// 	}
	// }
	//
	// if we reach here the tiles are the same, which was checked above.
	// panic("unreachable")

	// bits different for x and y
	xc := uint32(32 - bits.LeadingZeros32(t.X^tile.X))
	yc := uint32(32 - bits.LeadingZeros32(t.Y^tile.Y))

	// max of xc, yc
	maxc := xc
	if yc > maxc {
		maxc = yc

	}

	return Tile{
		X: t.X >> maxc,
		Y: t.Y >> maxc,
		Z: t.Z - Zoom(maxc),
	}
}

// Children returns the 4 children of the tile.
// Tiles at MaxZoom and above have no representable children.
func (t Tile) Children() Tiles {
	if t.Z >= MaxZoom {
		return nil
	}

	return Tiles{
		Tile{t.X << 1, t.Y << 1, t.Z + 1},
		Tile{(t.X << 1) + 1, t.Y << 1, t.Z + 1},
		Tile{(t.X << 1) + 1, (t.Y << 1) + 1, t.Z + 1},
		Tile{t.X << 1, (t.Y << 1) + 1, t.Z + 1},
	}
}

// Siblings returns the 4 tiles that share this tile's parent.
func (t Tile) Siblings() Tiles {
	return t.Parent().Children()
}

// Quadkey returns the quad key for the tile.
func (t Tile) Quadkey() uint64 {
	var i, result uint64
	for i = 0; i < uint64(t.Z); i++ {
		result |= (uint64(t.X) & (1 << i)) << i
		result |= (uint64(t.Y) & (1 << i)) << (i + 1)
	}

	return result
}

// Range returns the min and max tile "range" to cover the tile
// at the given zoom. Zooms above MaxZoom return invalid zero-coordinate
// endpoints at the requested zoom.
func (t Tile) Range(z Zoom) (min, max Tile) {
	if z > MaxZoom {
		invalid := Tile{Z: z}
		return invalid, invalid
	}

	if z < t.Z {
		t = t.toZoom(z)
		return t, t
	}

	offset := z - t.Z
	return Tile{
			X: t.X << offset,
			Y: t.Y << offset,
			Z: z,
		}, Tile{
			X: ((t.X + 1) << offset) - 1,
			Y: ((t.Y + 1) << offset) - 1,
			Z: z,
		}
}

func (t Tile) toZoom(z Zoom) Tile {
	if z > t.Z {
		return Tile{
			X: t.X << (z - t.Z),
			Y: t.Y << (z - t.Z),
			Z: z,
		}
	}

	return Tile{
		X: t.X >> (t.Z - z),
		Y: t.Y >> (t.Z - z),
		Z: z,
	}
}
