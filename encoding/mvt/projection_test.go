package mvt

import (
	"math"
	"testing"

	"github.com/paulmach/orb"
	"github.com/paulmach/orb/maptile"
	"github.com/paulmach/orb/project"
)

func TestNonPowerOfTwoProjection(t *testing.T) {
	tile := maptile.New(8956, 12223, 15)
	regProj := newProjection(tile, 4096)
	nonProj := nonPowerOfTwoProjection(tile, 4096)

	expected := loadGeoJSON(t, tile)
	layers := NewLayers(loadGeoJSON(t, tile))

	// loopy de loop of projections
	for _, l := range layers {
		for _, f := range l.Features {
			f.Geometry = project.Geometry(f.Geometry, regProj.ToTile)
		}
	}

	for _, l := range layers {
		for _, f := range l.Features {
			f.Geometry = project.Geometry(f.Geometry, nonProj.ToWGS84)
		}
	}

	for _, l := range layers {
		for _, f := range l.Features {
			f.Geometry = project.Geometry(f.Geometry, nonProj.ToTile)
		}
	}

	for _, l := range layers {
		for _, f := range l.Features {
			f.Geometry = project.Geometry(f.Geometry, regProj.ToWGS84)
		}
	}

	result := layers.ToFeatureCollections()

	xEpsilon, yEpsilon := tileEpsilon(tile)
	for key := range expected {
		for i := range expected[key].Features {
			r := result[key].Features[i]
			e := expected[key].Features[i]

			compareOrbGeometry(t, r.Geometry, e.Geometry, xEpsilon, yEpsilon)
		}
	}
}

func TestPowerOfTwoProjectionHighZoom(t *testing.T) {
	for _, tile := range []maptile.Tile{
		maptile.New((1<<21)-1, (1<<21)-1, 21),
		maptile.New(math.MaxUint32, math.MaxUint32, maptile.MaxZoom),
	} {
		powerOfTwo := newProjection(tile, DefaultExtent)
		nonPowerOfTwo := nonPowerOfTwoProjection(tile, DefaultExtent)
		point := tile.Center()

		if got, want := powerOfTwo.ToTile(point), nonPowerOfTwo.ToTile(point); !got.Equal(want) {
			t.Errorf("power-of-two projection differs at zoom %d: %v != %v", tile.Z, got, want)
		}

		point = orb.Point{DefaultExtent / 2, DefaultExtent / 2}
		got := powerOfTwo.ToWGS84(point)
		want := nonPowerOfTwo.ToWGS84(point)
		for _, coordinate := range []float64{got[0], got[1], want[0], want[1]} {
			if math.IsNaN(coordinate) || math.IsInf(coordinate, 0) {
				t.Fatalf("projection returned non-finite coordinate at zoom %d: %v != %v", tile.Z, got, want)
			}
		}
		xEpsilon, yEpsilon := tileEpsilon(tile)
		comparePoints(t, []orb.Point{want}, []orb.Point{got}, xEpsilon, yEpsilon)
	}
}

func TestProjectionZeroExtentUsesDefault(t *testing.T) {
	tile := maptile.New(8956, 12223, 15)
	zeroExtent := newProjection(tile, 0)
	defaultExtent := newProjection(tile, DefaultExtent)
	point := tile.Center()

	if got, want := zeroExtent.ToTile(point), defaultExtent.ToTile(point); !got.Equal(want) {
		t.Errorf("zero extent projection differs from default: %v != %v", got, want)
	}

	point = orb.Point{DefaultExtent / 2, DefaultExtent / 2}
	if got, want := zeroExtent.ToWGS84(point), defaultExtent.ToWGS84(point); !got.Equal(want) {
		t.Errorf("zero extent inverse projection differs from default: %v != %v", got, want)
	}
}
