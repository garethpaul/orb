# MVT Degenerate Segment Marshal Design

## Status: Accepted

## Problem

`mvt.Marshal` converts every coordinate to `int32` while writing geometry
commands. Consecutive source coordinates can therefore become the same encoded
point either because they are duplicates or because distinct floating-point
coordinates quantize to the same integer. The encoder currently emits a
`LineTo(0, 0)` parameter pair in both cases.

The [Mapbox Vector Tile 2.1 specification](https://github.com/mapbox/vector-tile-spec/tree/master/2.1)
requires that `LineTo` deltas must not both be zero. It also requires polygon
rings to contain more than one `LineTo` command and forbids the cursor position
before `ClosePath` from repeating the ring's first point. Explicitly closed
three-point rings currently lose the repeated endpoint during encoding and
therefore emit only one `LineTo` command.

## Constraints

- Preserve public APIs and valid geometry output.
- Validate the integer coordinates that are actually encoded, not only source
  floating-point equality.
- Return errors through the existing contextual `Marshal` path.
- Preserve path shape while removing only vertices that are indistinguishable
  in the integer coordinate space the format can represent.
- Preserve Go 1.20 compatibility.

## Options Considered

1. **Normalize redundant encoded vertices, then reject collapsed geometry.**
   Recommended because tile projection routinely creates redundant integer
   vertices, removing them preserves the representable path, and geometries
   that collapse below valid counts still return explicit errors.
2. Reject every repeated encoded vertex. Rejected because it breaks established
   projection pipelines even when enough distinct vertices remain for a valid
   command sequence.
3. Permit zero deltas for decoder compatibility. Rejected because the public
   encoder claims MVT output and the normative format explicitly forbids them.

## Decision

Extend geometry validation with integer-coordinate normalization helpers. Lines
remove adjacent vertices that encode to the same point and reject the result if
fewer than two encoded vertices remain. Rings remove adjacent redundant
vertices and an encoded closing coordinate, then require at least three encoded
vertices before `ClosePath`. Apply these checks at all nested multiline,
polygon, and multipolygon boundaries.

## Validation

- Observe focused public `Marshal` regressions fail for geometries that collapse
  below valid command counts, and verify redundant projected vertices are
  normalized without emitting zero deltas.
- Pass focused tests on Go 1.20.14 and Go 1.25.11.
- Run both pinned full Make gates, hostile mutations, hosted matrices, and
  CodeQL before merge.
