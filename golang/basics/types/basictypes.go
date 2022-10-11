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

	// Note, << operator is shifting a 1 bit left. for example, 1<<100 shifts
	// a 1 bit left 100 places. In other words, the binary number that is 1
	// followed by 100 zeroes.
	// Obviously, only 1 and 0 can be shifted as
	// we are in the base-2 binary. So, something like 2<<100 is not compilable.
	// >> operator does the reverse action. 1>>100 shifts a 1 bit right 100
	// places.

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

	fmt.Println("--- Type Inference")
	typeInference()

	fmt.Println("--- Type Conversion")
	typeConversion()

	fmt.Println("--- String Converstion")
	stringConversion()

	fmt.Println("--- Numeric Constants")
	numericConstants()
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
	// This string(int) will output the string of rune.
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

	fmt.Printf("a(%[1]T)=%[1]v, b(%[2]T)=%[2]v, c(%[3]T)=%[3]v, d(%[4]T)=%[4]v\n",
		a, b, c, d)

	if err != nil {
		fmt.Println(err)
	}
}

func numericConstants() {
	// Numeric constant are high-precision values

	// The following yields error as variable b infered to be int and int cannot
	// accept such a large number.
	// var big = 1 << 100

	// However, it can be done with constants
	const (
		huge = 1e1000
		Pi   = 3.14159265358979323846264338327950288419716939937510582097494459
		Pi2  = Pi / 2
		// Shifting a 1 bit to left by 100 places. i.e. the binary number
		// that is 1 followed by 100 zeros.
		big = 1 << 100

		// Shift it right again 99 places, so we end up with 1<<1 which is 2.
		small = big >> 99
	)
	// These numbers can't be assigned to printed, The yields overflow error,
	// as they should. However, they can be used in arithmatics, and that's
	// why they are important for precise calculation.
	// For example, using Pi in a calculation with the higher precision,
	// produce a better result
	pi := float64(Pi)

	fmt.Println("Pi with lost precision is", pi)
	// Note, that arithmatic with higher precision numbers carry the high
	// precision until the result is assigned.
	fmt.Println("Pi/2 with high precision", Pi*1.3897)
	fmt.Println("Pi/2 with low precision", pi*1.3897)

	// Another example
	fmt.Println(small * 10)  // 20
	fmt.Println(small * 0.1) // 0.2
	// The following throw a compiler error as it tries to convert big
	// to an int type which results in an overflow.
	// i := big

	f := big * 0.1
	// This can be done as Float64 can show large numbers by
	// losing the precision
	fmt.Printf("%v (%T)\n", f, f)

	// Note that the following returns a compiler error as int can store
	// maximum a 64-bit integer:
	// big := 1 << 100
	// So, only constant variables can define such bit numbers.

}
