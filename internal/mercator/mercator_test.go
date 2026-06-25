package mercator

import (
	"math"
	"testing"
)

func TestScalarMercator(t *testing.T) {
	x, y := ToPlanar(0, 0, 31)
	lat, lng := ToGeo(x, y, 31)

	if lat != 0.0 {
		t.Errorf("Scalar Mercator, latitude should be 0: %f", lat)
	}

	if lng != 0.0 {
		t.Errorf("Scalar Mercator, longitude should be 0: %f", lng)
	}

	x, y = ToPlanar(0, 0, 32)
	lng, lat = ToGeo(x, y, 32)
	if x != 1<<31 || y != 1<<31 || lng != 0 || lat != 0 {
		t.Errorf("Scalar Mercator, zoom 32 round trip incorrect: %f %f %f %f", x, y, lng, lat)
	}

	// specific case
	if x, y := ToPlanar(-87.65005229999997, 41.850033, 20); math.Floor(x) != 268988 || math.Floor(y) != 389836 {
		t.Errorf("Scalar Mercator, projection incorrect, got %v %v", x, y)
	}

	if x, y := ToPlanar(-87.65005229999997, 41.850033, 28); math.Floor(x) != 68861112 || math.Floor(y) != 99798110 {
		t.Errorf("Scalar Mercator, projection incorrect, got %v %v", x, y)
	}

	// default level
	for _, city := range Cities {
		x, y := ToPlanar(city[1], city[0], 31)
		lng, lat = ToGeo(x, y, 31)

		if math.Abs(lat-city[0]) > Epsilon {
			t.Errorf("Scalar Mercator, latitude miss match: %f != %f", lat, city[0])
		}

		if math.Abs(lng-city[1]) > Epsilon {
			t.Errorf("Scalar Mercator, longitude miss match: %f != %f", lng, city[1])
		}
	}

	// test polar regions
	if _, y := ToPlanar(0, 89.9, 31); y != (1<<31)-1 {
		t.Errorf("Scalar Mercator, top of the world error, got %v", y)
	}

	if _, y := ToPlanar(0, -89.9, 31); y != 0 {
		t.Errorf("Scalar Mercator, bottom of the world error, got %v", y)
	}
}
