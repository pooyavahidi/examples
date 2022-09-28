package main

import (
	"examples/hello/farewell"
	"fmt"

	"my-module/greetings"
	"my-module/greetings/deutsch"
)

func main() {
	// Print from our own greetings module
	message := greetings.Hello("mate")
	fmt.Println(message)

	// Print from another package in greetings module
	fmt.Println(deutsch.GutenTag())

	// Print from the Quote function which calls an external module
	fmt.Println(GetQuote())

	// Print from farewell package within the current module
	fmt.Println(farewell.Farewell("mate"))

	// The following will result in compile error as unexported functions are not
	// accessible outside of a package:
	// farewell.unexportedFunc()
}
