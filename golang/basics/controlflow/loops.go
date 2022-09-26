package main

import (
	"fmt"
)

func main() {
	// Go has only one looping construct which is `for` loop.

	// Traditional for loop
	for i := 0; condition(i); i = post(i) {
		fmt.Println("execute body with index", i)
		fmt.Println("---------")
	}
	fmt.Println("exit the loop")

	// The init and post statements are optional

	// Traditional while loop
	var i int
	for i < 5 {
		fmt.Println(i)
		i++
	}

	// Traditional infinite loop
	i = 0
	for {
		fmt.Println(i)
		i++
		if i == 5 {
			break
		}
	}
}

func post(index int) int {
	index++
	fmt.Println("increase index from", index-1, "to", index)
	return index
}

func condition(index int) bool {
	fmt.Println("check condition if", index, "is bigger than 5")
	if index < 5 {
		return true
	} else {
		return false
	}
}
