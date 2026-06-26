package wkb

import (
	"encoding/binary"
	"errors"
	"testing"
)

func TestHighBitElementCountsAreNotAcceptedAsEmpty(t *testing.T) {
	for _, geometryType := range []uint32{
		multiPointType,
		lineStringType,
		multiLineStringType,
		polygonType,
		multiPolygonType,
		geometryCollectionType,
	} {
		data := make([]byte, 9)
		data[0] = 1
		binary.LittleEndian.PutUint32(data[1:5], geometryType)
		binary.LittleEndian.PutUint32(data[5:9], 0x80000000)

		if _, err := Unmarshal(data); !errors.Is(err, ErrNotWKB) {
			t.Fatalf("geometry type %d accepted high-bit count: %v", geometryType, err)
		}
	}
}
