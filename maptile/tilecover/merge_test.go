package tilecover

import (
	"testing"

	"github.com/paulmach/orb/maptile"
)

func TestMergeUp(t *testing.T) {
	f := loadFeature(t, "./testdata/line.geojson")

	tiles := Geometry(f.Geometry, 15)
	c1 := len(MergeUpPartial(tiles, 1, 1))

	tiles = Geometry(f.Geometry, 15)
	c2 := len(MergeUpPartial(tiles, 1, 2))

	tiles = Geometry(f.Geometry, 15)
	c3 := len(MergeUpPartial(tiles, 1, 3))

	tiles = Geometry(f.Geometry, 15)
	c4 := len(MergeUpPartial(tiles, 1, 4))

	tiles = Geometry(f.Geometry, 15)
	c := len(MergeUp(tiles, 1))

	if c1 > c2 {
		t.Errorf("c1 should be bigger than c2: %v != %v", c1, c2)
	}

	if c2 > c3 {
		t.Errorf("c2 should be bigger than c3: %v != %v", c2, c3)
	}

	if c3 > c4 {
		t.Errorf("c3 should be bigger than c4: %v != %v", c3, c4)
	}

	if c4 != c {
		t.Errorf("count 4 should be same as mergeUp: %v != %v", c4, c)
	}
}

func TestMergeUpAboveMaximumZoom(t *testing.T) {
	tile := maptile.Tile{Z: maptile.MaxZoom + 1}

	for _, merge := range []struct {
		name string
		fn   func(maptile.Set) maptile.Set
	}{
		{name: "complete", fn: func(set maptile.Set) maptile.Set { return MergeUp(set, 0) }},
		{name: "partial", fn: func(set maptile.Set) maptile.Set { return MergeUpPartial(set, 0, 4) }},
	} {
		t.Run(merge.name, func(t *testing.T) {
			set := maptile.Set{tile: true}
			result := merge.fn(set)
			if len(result) != 1 || !result[tile] {
				t.Fatalf("above-maximum tile must remain unchanged: %v", result)
			}
		})
	}
}

func TestMergeUpPreservesSetWhenMinimumExceedsInputZoom(t *testing.T) {
	tile := maptile.New(1, 1, 2)

	for _, merge := range []struct {
		name string
		fn   func(maptile.Set) maptile.Set
	}{
		{name: "complete", fn: func(set maptile.Set) maptile.Set { return MergeUp(set, 3) }},
		{name: "partial", fn: func(set maptile.Set) maptile.Set { return MergeUpPartial(set, 3, 4) }},
	} {
		t.Run(merge.name, func(t *testing.T) {
			result := merge.fn(maptile.Set{tile: true})
			if len(result) != 1 || !result[tile] {
				t.Fatalf("minimum above input zoom must preserve the tile: %v", result)
			}
		})
	}
}

func TestMergeUpPreservesNonuniformZoomSets(t *testing.T) {
	sets := []struct {
		name string
		set  maptile.Set
	}{
		{
			name: "mixed representable zooms",
			set: maptile.Set{
				maptile.New(1, 1, 2): true,
				maptile.New(2, 2, 3): true,
			},
		},
		{
			name: "mixed representable and excessive zooms",
			set: maptile.Set{
				maptile.New(1, 1, 2):                 true,
				{Z: maptile.MaxZoom + 1, X: 1, Y: 1}: true,
			},
		},
	}

	for _, input := range sets {
		for _, merge := range []struct {
			name string
			fn   func(maptile.Set) maptile.Set
		}{
			{name: "complete", fn: func(set maptile.Set) maptile.Set { return MergeUp(set, 0) }},
			{name: "partial", fn: func(set maptile.Set) maptile.Set { return MergeUpPartial(set, 0, 4) }},
		} {
			t.Run(input.name+"/"+merge.name, func(t *testing.T) {
				result := merge.fn(cloneSet(input.set))
				if len(result) != len(input.set) {
					t.Fatalf("nonuniform zoom set must remain unchanged: %v", result)
				}
				for tile := range input.set {
					if !result[tile] {
						t.Fatalf("nonuniform zoom set lost tile %v: %v", tile, result)
					}
				}
			})
		}
	}
}

func BenchmarkMergeUp_z0z10(b *testing.B) {
	g := loadFeature(b, "./testdata/russia.geojson").Geometry
	tiles := Geometry(g, 10)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeUp(cloneSet(tiles), 0)
	}
}

func BenchmarkMergeUp_z8z9(b *testing.B) {
	g := loadFeature(b, "./testdata/russia.geojson").Geometry
	tiles := Geometry(g, 9)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeUp(cloneSet(tiles), 8)
	}
}

func BenchmarkMergeUpPartial4_z0z10(b *testing.B) {
	g := loadFeature(b, "./testdata/russia.geojson").Geometry
	tiles := Geometry(g, 10)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeUpPartial(cloneSet(tiles), 0, 4)
	}
}

func BenchmarkMergeUpPartial4_z8z9(b *testing.B) {
	g := loadFeature(b, "./testdata/russia.geojson").Geometry
	tiles := Geometry(g, 9)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeUpPartial(cloneSet(tiles), 8, 4)
	}
}

func cloneSet(t maptile.Set) maptile.Set {
	r := make(maptile.Set, len(t))
	for k, v := range t {
		if v {
			r[k] = v
		}
	}

	return r
}
