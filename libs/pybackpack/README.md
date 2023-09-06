# pybackpack
A collection of utilities, helpers and tools in Python.

## cli module
A few classes to make implementation of cli tools more organized. It uses composite
pattern for creating the parsers and subcommands. It also uses function decorators which
identity which function has to be executed for the provided arguments.
The idea behind this module is to encapsulate each parser and it’s arguments, and the corresponding handler function.

Look at the `tests/cli/my_cli.py` for a multi sub-commands example.