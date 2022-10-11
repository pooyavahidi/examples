package farewell

import "fmt"

func Farewell(name string) string {
	return fmt.Sprintf("Bye, %v.", name)
}

// Functions which starts with lower case are not exported. So, they are not
// accessible from outside the package.
func unexportedFunc() {
	fmt.Println("From farewell.privateFunc")
}
