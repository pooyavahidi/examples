package main

import "fmt"

// Package level variables. Their name are usually longer than function level
// variables and can't be defined using the := construct.
var variable1 bool

// So, this is no possible at the package level:
// variable2 := bool

func main() {
	// Function level variables. They are usually have short names.
	var i int

	var f float64

	r := "ready"

	// Variable declaration also initialize the variable to it's zero value.
	// zero value for numeric types is 0
	// zero value for boolean is false
	// zero value for string is ""
	fmt.Println(i, f, variable1, r)

	// A variable can be defined in the 4 following ways:
	a := ""           // Commonly used for function variables
	var b string      // Commonly used for package variables
	var c = ""        // Usually used when declaring multiple variables
	var d string = "" // Rarly used.

	fmt.Printf("%q %q %q %q\n", a, b, c, d)

	multipleDeclarations()
}

func multipleDeclarations() {
	// Declare multiple variables and initialize them at the same time
	var a, b, c = "val1", "val2", "val3"

	// Declare multiple variable of a same type
	var i, j int = 1, 2
	// It can be simplified
	var x, y = 1, 2

	fmt.Println(a, b, c, i, j, x, y)
}
