package greetings

import (
	"errors"
	"fmt"
)

// Internal package level constant variable. This is read only and only visible
// within the package
const supportedLanguage = "Deutsch"

// Exported package level constant variable. This is read only but visible to
// within and outside of this package.
const Version = 0.1

// Exported package level variable, this is visible to external packages and
// can be modified outside of this package. Similar to above, package level
// variables can be defined as internal or exported.
var ShowInfo bool

// Hello returns a greeting for the named person.
func Hello(name string) (string, error) {
	// Pring some info
	if ShowInfo {
		fmt.Println("Info from the greetings package.",
			"supportedLanguage = ", supportedLanguage)
	}
	// If no name was given, return an error with a message
	if name == "" {
		return "", errors.New("empty name")
	}

	// If a name was received, return a value that embeds the name
	// in a greeting message.
	message := fmt.Sprintf("Hi, %v. Welcome!", name)
	return message, nil
}
