# Workspaces and multi module development

I created `go.work` file by running the following command in the parent directory
(aka *workspace* directory).
```sh
go work init ./hello
```

Now from the parent directory we can runt the hello module by this command:
```sh
go run examples/hello
```
The Go command includes modules in the workspace as main modules. This allows
us to refer to a package in the mdoule, even outside the module.

## Add another module to the workspace
Now we add *greetings* module using `go work` command.
```sh
go work use ./greetings
```

For further reading on how to clone and external module in this workspace and develop on across modules at the same time, see this [link](https://go.dev/doc/tutorial/workspaces).