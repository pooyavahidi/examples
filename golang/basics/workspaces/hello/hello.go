package main

import (
	"examples/hello/farewell"
	"fmt"
	"log"
	"my-module/greetings"
	"my-module/greetings/deutsch"

	"golang.org/x/example/stringutil"
)

func main() {
	// Set properties of the predefined Logger, including the log entry prefix
	// and a flag to disable printing the time stamp, source file, line number.
	log.SetPrefix("greetings: ")
	log.SetFlags(0)

	// If an error was returned, print it to the console and exit the program.
	message, err := greetings.Hello("mate")
	if err != nil {
		log.Fatal(err)
	}

	// If no error was returned, print from our own greetings module to
	// the console
	fmt.Println(message)

	// Print from another package in greetings module
	fmt.Println(deutsch.GutenTag())

	// Print from the Quote function which calls an external module
	message = GetQuote()
	fmt.Println(message)

	// Print a reverse word using the external modul golang.org/x/example
	fmt.Println("Reverse of Hello is", stringutil.Reverse("Hello"))

	// Print from farewell package within the current module
	fmt.Println(farewell.Farewell("mate"))
}
