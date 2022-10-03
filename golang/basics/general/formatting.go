package main

import (
	"fmt"
	"os"
)

func main() {
	// For further details
	// https://pkg.go.dev/fmt

	// This is the same pattern for all formatting and printing functions
	// across go standard library.
	//	S<funcName>()		Print to a string
	//	F<funcName()		Print to io.Writer
	//	<funcName>()		Print to stdout
	//
	//  <funcName>f()		Print with formatting
	//	<funcName>ln()		Print with a newline at the end

	s := "Earth"
	// Print to stdout without any formatting
	fmt.Print(s, "\n")
	fmt.Println("Planet", s, "is our home")
	fmt.Printf("Planet %v is our home, for now!\n", s)

	// Print to io.Writer
	_, err := fmt.Fprint(os.Stdout, "Planet ", s, "\n")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
	}

	// Print to a string
	var r string
	r = fmt.Sprint("Planet ", s)
	fmt.Println(r)
	r = fmt.Sprintf("Planet %v", s)
	fmt.Println(r)

	argumentIndexes()
}

func argumentIndexes() {
	// We can use argument indexes explicitly. The [n] notation before the
	// verb indicates that nth argument is to be formatted instead.
	// Note, the index here starts from 1.
	s := "Earth"
	fmt.Printf("Planet %[1]v\n", s)

	// We can repeat a variable using the its index.
	c := "blue"
	fmt.Printf("Planet %[1]v is our home. %[1]v is %[2]v", s, c)

}
