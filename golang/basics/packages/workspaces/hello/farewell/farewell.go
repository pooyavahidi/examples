package farewell

import "fmt"

// Exported package level variable which will be accessible from outside of
// this package
var EndingPunctuation string = "."

// un-exported package level variable which be only accessible within
// this package
var openning string = "Bye"

func Farewell(name string) string {
	return fmt.Sprintf("%v, %v%v", openning, name, EndingPunctuation)
}
