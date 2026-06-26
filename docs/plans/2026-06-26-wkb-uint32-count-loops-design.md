# WKB Architecture-Safe Count Loop Design

Status: Completed

## Problem

WKB element counts are decoded as `uint32`, but six decoder loops convert the
count to architecture-sized `int`. The Go specification defines `int` as 32 or
64 bits and integer conversions truncate without reporting overflow. On a
32-bit build, a count such as `0x80000000` becomes negative, skips the loop, and
can turn truncated WKB into a successfully decoded empty geometry.

## Options

1. Reject every count above `MaxInt`. This introduces an architecture-specific
   input limit and changes the decoder's existing streaming semantics.
2. Add a new global geometry-size limit. This is a larger API and compatibility
   decision unrelated to the conversion bug.
3. Iterate with a `uint32` index. This preserves the wire type and current
   allocation caps while ensuring malformed input reaches a read and fails.

## Decision

Use option 3 for all six point, line, polygon, and collection count loops. Add
a Linux/386 package test because the regression is not observable on 64-bit
architectures.

## Validation

- RED: `GOARCH=386 go test ./encoding/wkb` accepts high-bit counts before the
  loop fix and fails the new regression.
- GREEN: both native and Linux/386 WKB tests pass after all loops use `uint32`.
- Static contracts reject `int(num)` loop bounds and require the 386 gate.
- Run `make check` on Go 1.20.14 and Go 1.25.11.
