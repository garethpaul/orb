Package orb/resample has a couple functions for resampling line geometry
into more or less evenly spaces points.

	func Resample(ls orb.LineString, df orb.DistanceFunc, totalPoints int) orb.LineString
	func ToInterval(ls orb.LineString, df orb.DistanceFunc, dist float64) orb.LineString

For example, resampling a line string so the points are 1 planar unit apart:

	ls := resample.ToInterval(ls, planar.Distance, 1.0)

Both entry points return `nil` for invalid numeric input, nil distance
callbacks, non-finite coordinates or callback distances, non-progressing
spacing, and requests that exceed the 64 MiB output point budget.
