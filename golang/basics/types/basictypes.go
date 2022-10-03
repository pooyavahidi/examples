package main

import (
	"fmt"
	"math/cmplx"
	"strconv"
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

	typeInference()
	typeConversion()
	stringConversion()
}

func typeInference() {
	// When a variable declared without explicit type, the variable's type is
	// inferred from the value on the right hand side.

	f := 2.35 // float64

	a := f // a is type of float64

	fmt.Printf("a is of type %T\n", a)

}
func typeConversion() {
	var i int = 5
	var f float64 = float64(i)
	var u uint = uint(f)

	fmt.Println(i, f, u)

	// The simplifed version of above
	a := 5
	b := float64(a)
	c := uint(b)

	fmt.Println(a, b, c)

	// Unlike C, Go requires explicit conversion, the following raises complie
	// error:
	// 		var d int = 5
	// 		var e float64 = d
}

func stringConversion() {
	var i int = 5

	s := string(i)
	// This string(int) will output the rune of given value
	fmt.Printf("String of %v is %q\n", i, s)

	// The most common way of numeric conversion is using Atoi (string to int)
	// and Itoa (int to string) functions in strconv package.
	s = strconv.Itoa(i)
	fmt.Printf("String of %v is %q\n", i, s)

	// Conver from string
	i, err := strconv.Atoi("5")
	fmt.Println(i)

	// Parse string to other types
	a, err := strconv.ParseInt("5", 10, 32)
	b, err := strconv.ParseUint("5", 10, 32)
	c, err := strconv.ParseBool("true")
	d, err := strconv.ParseFloat("5.32", 32)

	fmt.Printf("a(%[1]T)=%[1]v, b(%[2]T)=%[2]v, c(%[3]T)=%[3]v, d(%[4]T)=%[4]v",
		a, b, c, d)

	if err != nil {
		fmt.Println(err)
	}

}
