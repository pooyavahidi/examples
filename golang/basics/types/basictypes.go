package main

import (
	"fmt"
	"math/cmplx"
)

var (
	ToBe bool   = false
	Name string = "Test"
	// int and uint are 64-bits wide in 64-bit systems.
	// However, `int`` is a signed integer, so it has only 63 bits available
	// for storing the digits.

	// When you need integer, you should use `int` unless you have a specific
	// reason to use a sized or unsigned integer.
	MaxInt      int    = 1<<63 - 1
	MaxInt8     int8   = 1<<7 - 1
	MaxInt16    int16  = 1<<15 - 1
	MaxInt32    int32  = 1<<31 - 1
	MaxInt64    int64  = 1<<63 - 1
	UnsignedInt uint   = 1<<64 - 1
	MaxUInt8    uint8  = 1<<8 - 1
	MaxUInt16   uint16 = 1<<16 - 1
	MaxUInt32   uint32 = 1<<32 - 1
	MaxUInt64   uint64 = 1<<64 - 1

	// Numbers with decimal point
	Float32 float32 = 1.5
	Float64 float64 = 0.009

	// alias for uint8
	Byte byte = 1<<8 - 1

	// alias for int32, represent a Unicode code point
	Rune rune = rune(0x03A3) // Unicode for Sigma character

	// Complex numbers
	z64  complex64  = 0i
	z128 complex128 = cmplx.Sqrt(-5 + 12i)
)

func main() {
	fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
	fmt.Printf("Type: %T Value: %v\n", Name, Name)
	fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt)
	fmt.Printf("Type: %T Value: %v\n", UnsignedInt, UnsignedInt)
	fmt.Printf("Type: %T Value: %v\n", MaxUInt64, MaxUInt64)
	fmt.Printf("Type: %T Value: %v Character: %c\n", Rune, Rune, Rune)
	fmt.Printf("Type: %T Value: %v\n", z64, z64)
	fmt.Printf("Type: %T Value: %v\n", z128, z128)
}
