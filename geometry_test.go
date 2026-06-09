package orb

import (
	"fmt"
	"testing"
)

func TestGeometryDimensions(t *testing.T) {
	cases := []struct {
		Geometry   Geometry
		Dimensions int
	}{
		{Point{}, 0},
		{MultiPoint{}, 0},
		{LineString{}, 1},
		{MultiLineString{}, 1},
		{Ring{}, 2},
		{Polygon{}, 2},
		{MultiPolygon{}, 2},
		{Bound{}, 2},
		{Collection{Point{}, LineString{}}, 1},
	}

	for _, tc := range cases {
		t.Run(fmt.Sprintf("type: %T", tc.Geometry), func(t *testing.T) {
			if v := tc.Geometry.Dimensions(); v != tc.Dimensions {
				t.Errorf("incorrect dimensions: %v", v)
			}
		})
	}
}

func TestCollectionDimensionsSkipsNilGeometries(t *testing.T) {
	cases := []struct {
		name       string
		collection Collection
		dimensions int
	}{
		{
			name:       "nil geometry collection dimensions",
			collection: Collection{nil},
			dimensions: -1,
		},
		{
			name:       "nil geometry before point",
			collection: Collection{nil, Point{}},
			dimensions: 0,
		},
		{
			name:       "nil geometry between higher dimensions",
			collection: Collection{LineString{}, nil, Polygon{}},
			dimensions: 2,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if v := tc.collection.Dimensions(); v != tc.dimensions {
				t.Errorf("incorrect dimensions: %v != %v", v, tc.dimensions)
			}
		})
	}
}

func TestCollectionBound(t *testing.T) {
	// from the empty Point we get the zero bound.
	expected := Bound{}

	b2 := Collection(AllGeometries).Bound()
	if !b2.Equal(expected) {
		t.Errorf("wrong bound: %v != %v", b2, expected)
	}
}
