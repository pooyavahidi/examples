"""Cli related classes and decorators.

classes to create parser commmands using composite pattern and execute desired
actions by creating functions and decorate them as cli handlers.

"""

import sys
import argparse
import traceback


class ParserComposite:
    """Base class for the Parser commands

    Each command is a ParserComposite, if it is a parent to other
    ParserComposite objects, it's a composite. If it has no children, it's a
    leaf.

    Key Attributes:
        name = name of this command which will be used in the cli.
        parent = parent is an object of type ParserComposite which act as the
                 parent command.
        parser = it's the argparsse parser for this command.
    """

    def __init__(self, name=None, parent=None, **kwargs):
        self._parent = parent
        self._sub_parsers = None
        self.name = name
        self.parser = None

        if parent:
            # If this is a child of another composite
            self.parser = parent._sub_parsers.add_parser(name=name, **kwargs)
        else:
            # if this is the root and there is no parent
            self.parser = argparse.ArgumentParser(**kwargs)

    def _add_sub_parsers(self, **kwargs):
        command_index = 0
        if self._parent:
            command_index = (
                int(self._parent._sub_parsers.dest.split("_")[1]) + 1
            )

        kwargs["dest"] = f"command_{command_index}"
        self._sub_parsers = self.parser.add_subparsers(**kwargs)


def cli_handler(runner, commands=None):
    """Decorator for cli handler functions"""

    def decorator_cli_handler(func):
        # Register this function to the cli handlers list
        runner.add_handler(func, commands)
        return func

    return decorator_cli_handler


class CliRunner:
    """This class runs the regsitered handlers based on the provided arguments.
    Normally only one instance of this class is needed. It holds the dictionary
    of handlers and map them to the provided commands from the cli.
    """

    def __init__(self):
        self.handlers = dict()
        self.parser = None

    def add_handler(self, handler_func, commands=None):
        if commands:
            self.handlers["_".join(commands)] = handler_func
        else:
            # Default handler for Root command
            self.handlers["_"] = handler_func

    def __get_handler_key(self, args):
        args_dict = vars(args)
        # Get the all the provided commands in the Namespace
        commands_count = len(
            [x for x in args_dict.keys() if x.startswith("command_")]
        )

        # Looping through all the provided commands and concat them together
        # to construct the handler's key
        commands = []
        for i in range(commands_count):
            command = args_dict.get(f"command_{i}")
            if command:
                commands.append(command)

        # If there is any command provided, then it overrides the handler_key
        # with the one which matches the given commands
        if commands:
            handler_key = "_".join(commands)
        else:
            # Handler_key of "_" points to a specific handler function
            # which handles all the command agnostic arguments,
            # e.g. --verbose, --version
            handler_key = "_"

        return handler_key

    def __get_handler(self, args):
        handler_key = self.__get_handler_key(args)
        func = self.handlers.get(handler_key)
        if not func:
            sys.stderr.writelines(f"No handler for command: {handler_key}\n")
            self.parser.print_help()
            exit(1)
        return func

    def __create_input_variables(self, args, props):
        input_variables = vars(args)

        # Clean up the command_* keys from the variables
        commands = [
            x for x in input_variables.keys() if x.startswith("command_")
        ]
        for cmd in commands:
            input_variables.pop(cmd)

        input_variables["props"] = props
        return input_variables

    def run(self, parser, props=None, override_args=[]):
        """Runs the handler with provided arguments.

        This function parses the arguments, finds the relevant handler based
        on the provided arguments, and executes it.
        """
        self.parser = parser

        # Apply overriding arguments if provided
        if override_args:
            args = parser.parse_args(override_args)
        else:
            args = parser.parse_args()

        handler = self.__get_handler(args)
        # Construct input variables for handlers. Do some clean up and add
        # combine all of the arguements and props into one dictionary
        input_variables = self.__create_input_variables(args, props)
        try:
            res = handler(**input_variables)
        except:
            traceback.print_exc()
            exit(2)

        # If handler returns False, it means it counldn't handle it,
        # hence, showing the usage with exit code = 1
        if res is False:
            self.parser.print_help()
            exit(1)
