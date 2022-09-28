package main

import "fmt"

// Go's declarations read left to right which is easier to understand than C's.
// https://go.dev/blog/declaration-syntax

// Input variables
// /////////////////////////
func add(a int, b int) {
	fmt.Println(a + b)
}

// The above function with a shorter declaration.
func addWithShortDeclaration(a, b int) {
	fmt.Println(a + b)
}

// Results
// /////////////////////////
func multiply(a, b int) int {
	return a * b
}

// Multiple results
func divide(n, d int) (int, int) {
	// Integer division. Decimal is truncated.
	q := n / d
	// Remainder
	r := n % d

	return q, r
}

// Named return values
func divideWithNamedReturnVals(n, d int) (quotient, remainder int) {
	// Integer division. Decimal is truncated.
	quotient = n / d
	// Remainder
	remainder = n % d

	return quotient, remainder
}

// Named return values, with naked return
func divideWithNakedReturn(n, d int) (quotient, remainder int) {
	// Integer division. Decimal is truncated.
	quotient = n / d
	// Remainder
	remainder = n % d

	// return without any arguments returns the named return values. This called
	// "naked" return. Generally, it should be only used in short function.
	return
}
func main() {
	add(2, 4)
	addWithShortDeclaration(2, 4)

	fmt.Println(multiply(3, 4))
	fmt.Println(divide(17, 2))
	fmt.Println(divideWithNamedReturnVals(17, 2))
	fmt.Println(divideWithNakedReturn(17, 2))
}
