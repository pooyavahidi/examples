package main

import "rsc.io/quote"

func GetQuote() string {
	// Return from quote package
	return quote.Go()
}
