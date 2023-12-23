import sys
from enum import Enum
from abc import ABC
from dataclasses import dataclass
from typing import Any
import math
import logging
import inspect

# import boto3

# set level to error for sagemaker
logging.getLogger("sagemaker.config").setLevel(logging.ERROR)
# import sagemaker

# sagemaker_client = boto3.client("sagemaker")
# iam = boto3.client("iam")

command_outputs = []
service_commands = {}
SERVICE_PATH_SEPARATOR = "/"


class FontColor(Enum):
    """Font color for printing."""

    RESET = "\033[0m"
    RED = "\033[31m"
    RED_BRIGHT = "\033[91m"
    BLUE = "\033[34m"
    BLUE_BRIGHT = "\033[94m"
    GREEN = "\033[32m"
    GREEN_BRIGHT = "\033[92m"
    YELLOW = "\033[33m"
    YELLOW_BRIGHT = "\033[93m"
    MAGENTA = "\033[35m"
    MAGENTA_BRIGHT = "\033[95m"
    CYAN = "\033[36m"
    CYAN_BRIGHT = "\033[96m"
    WHITE = "\033[37m"
    WHITE_BRIGHT = "\033[97m"
    BLACK = "\033[30m"
    BLACK_BRIGHT = "\033[90m"


def print_color(text, font_color, **kwargs):
    """Print text in color."""
    print(font_color.value + str(text) + FontColor.RESET.value, **kwargs)


@dataclass
class CommandResult:
    """Represents the result of a command execution."""

    output: Any
    succeeded: bool = True
    error: Any = None
    error_message: str = None
    metadata: Any = None


class Command(ABC):
    """Interface for all commands."""

    def run(self, cmd_input, **kwargs) -> Any:
        """This method runs the command and return the result.
        This method should not raise any exception, instead, it returns
        a CommandResult object with the error and error_message"""
        raise NotImplementedError


def run_command(command: Command, cmd_input: Any, **kwargs) -> CommandResult:
    """Run a command and return the result."""
    try:
        result = command.run(cmd_input, **kwargs)
        return CommandResult(output=result)
    except Exception as ex:
        return CommandResult(
            output=None, succeeded=False, error=ex, error_message=str(ex)
        )


# Decorator for registering commands
def cli_command(name, groups=None, parameters=None, description=None):
    """Decorator for registering commands.
    Arguments:
        name: is the name of the command.
        groups: is a list of group paths which the command belongs to.
        parameters: is a dictionary of parameters with the following format:
        {
            "parameter_name": {
                "required": True,
                "description": "description of the parameter"
            },
        }
    """

    def decorator(obj):
        obj._cli_metadata = {
            "name": name,
            "groups": groups or [],
            "parameters": parameters or {},
            "description": description or obj.__doc__,
        }
        return obj

    return decorator


#####################
def register_commands(modules):
    for module in modules:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if hasattr(obj, "_cli_metadata"):
                metadata = obj._cli_metadata
                # Process each group path
                process_group_path(
                    service_commands,
                    metadata["groups"] or ["default"],
                    metadata,
                    obj,
                )


def process_group_path(root, group_paths, metadata, obj):
    for path in group_paths:
        if path in ["", "default"]:
            # Add command under the root if no specific group is defined
            root.setdefault("commands", [])
            add_command(root["commands"], metadata, obj)
        else:
            parts = path.split(SERVICE_PATH_SEPARATOR)
            # Add "groups" key if it doesn't exist
            root.setdefault("groups", [])

            current_level = root["groups"]
            for part in parts:
                # Find or create the group
                group = next(
                    (g for g in current_level if g["name"] == part), None
                )
                if not group:
                    group = {"name": part, "commands": [], "groups": []}
                    current_level.append(group)
                current_level = group["groups"]

            # Add the command to the "commands" list of the final group
            add_command(group["commands"], metadata, obj)


def add_command(commands_list, metadata, obj):
    command_name = metadata["name"]
    # Check for duplicate command name
    if any(cmd["name"] == command_name for cmd in commands_list):
        raise ValueError(f"Duplicate command name '{command_name}'.")
    commands_list.append({"name": command_name, "command": obj})


def format_size(size):
    """Convert size from bytes to a human-readable format."""
    if not size:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, i)
    size = round(size / power, 2)
    return f"{size}{size_name[i]}"


def format_datetime(datetime_str):
    return datetime_str.strftime("%Y-%m-%d %H:%M:%S")


def print_list(rows):
    """
    # Example usage
    rows = ["a", "b", "c"]
    """
    if not rows:
        return

    for row in rows:
        # print index for each row
        print_color(rows.index(row), FontColor.BLUE, end="\t")
        print(row)


def print_table(rows):
    """
    # Example usage
    rows = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]
    """
    if not rows:
        return

    headers = rows[0].keys()
    col_widths = {header: len(header) for header in headers}

    # Find the maximum width for each column
    for row in rows:
        for header in headers:
            col_widths[header] = max(
                col_widths[header], len(str(row.get(header, "")))
            )

    # Create a format string for each row
    row_format = "\t".join(
        ["{:<" + str(col_widths[header]) + "}" for header in headers]
    )

    # Print headers
    print(row_format.format(*headers))

    # Print rows
    for row in rows:
        print(
            row_format.format(
                *(str(row.get(header, "")) for header in headers)
            )
        )


@cli_command(name="test")
class Test(Command):
    """Test command."""

    def run(self, cmd_input, **kwargs):
        rows = [
            {
                "Name": "Alice",
                "Age": 30,
                "City": "New York",
                "Extra": {"a": 1},
            },
            {
                "Name": "Bob - or a very longer than expected name",
                "Age": 25,
                "City": "Los Angeles",
            },
            {
                "Name": "Charlie",
                "Age": 35,
                "City": "Chicago",
            },
        ]
        return rows


@cli_command(name="test2", groups=["default", "sm/ep"])
class Test2(Command):
    """Test command."""

    def run(self, cmd_input, **kwargs):
        return CommandResult("This is a test2.")


@cli_command(name="test", groups=["sm"])
class SageMakerTest(Command):
    """SageMaker test command."""

    def run(self, cmd_input, **kwargs):
        return CommandResult("This is a sagemaker test.")


# @clicommand(alias="test", groups=["sm:ep"])
# class SageMakerEndPointTest(Command):
#     """sagemaker endpoint test command."""

#     def run(self, cmd_input, **kwargs):
#         return CommandResult("This is a sagemaker endpoint test.")


@cli_command(name="bucket", groups=["sm"])
class SageMakerBucket(Command):
    """SageMaker bucket command."""

    def run(self, cmd_input, **kwargs):
        return CommandResult(sagemaker.Session().default_bucket())


@cli_command(name="ls", groups=["sm/ep"])
class SageMakerEndpointList(Command):
    """SageMaker endpoint list command."""

    def run(self, cmd_input, **kwargs):
        endpoints = sagemaker_client.list_endpoints()
        return CommandResult(
            [endpoint["EndpointName"] for endpoint in endpoints["Endpoints"]]
        )


@cli_command(
    name="desc",
    groups=["sm/ep"],
    parameters={"name": {"required": True, "desc": "endpoint name"}},
)
class SageMakerEndpointDescribe(Command):
    """SageMaker endpoint describe command."""

    def run(self, cmd_input, **kwargs):
        desc = sagemaker_client.describe_endpoint(
            EndpointName=cmd_input["name"]
        )
        return CommandResult(
            [
                {
                    "Name": desc["EndpointName"],
                    "ConfigName": desc["EndpointConfigName"],
                    "Status": desc["EndpointStatus"],
                    "CreationTime": format_datetime(desc["CreationTime"]),
                    "LastModifiedTime": format_datetime(
                        desc["LastModifiedTime"]
                    ),
                }
            ]
        )


# def handle_action(services, service_alias, action, args):
#     # Check if the service and action are supported
#     if service_alias not in services:
#         print(f"Service '{service_alias}' is not supported.")
#         return
#     if action not in services[service_alias]["commands"]:
#         print(f"Action '{action}' for '{service_alias}' is not supported.")
#         return

#     # Get the command class
#     command_class = services[service_alias]["commands"][action]

#     # Create an instance of the command class
#     command_instance = command_class()

#     # Call the run method and handle the result
#     try:
#         result = command_instance.run(args)
#         return handle_result(result)
#     except Exception as ex:
#         print(f"Error executing command '{action}': {ex}")


# def handle_action(services, service_alias, action, args):
#     # Check if the service is supported
#     if service_alias not in services:
#         print(f"Service '{service_alias}' is not supported.")
#         return

#     # Get the service
#     service = services[service_alias]["service"]

#     # Format action to match the method name in the class
#     method_name = action.replace("-", "_")

#     # Check if the action is callable and supported
#     if not hasattr(service, method_name) or not inspect.isroutine(
#         getattr(service, method_name)
#     ):
#         print(f"Action '{action}' for '{service_alias}' is not supported.")
#         return

#     # Remove unnecessary arguments before calling the method
#     args.pop("service", None)
#     args.pop("action", None)

#     # Call the method and handle the result
#     method = getattr(service, method_name)
#     try:
#         result = method(**args)
#         return handle_result(result)
#     except TypeError as ex:
#         print(f"Error calling action '{action}': {ex}")


# def create_parsers(service_commands, description=None, parent_parser=None):
#     if parent_parser is None:
#         parser = argparse.ArgumentParser(description=description)
#         subparsers = parser.add_subparsers(dest="sub_command")
#     else:
#         parser = parent_parser
#         subparsers = parent_parser.add_subparsers(dest="sub_command")

#     # Add default commands to each level of the parser
#     for cmd_name, cmd_class in service_commands["default"]["commands"].items():
#         cmd_parser = subparsers.add_parser(cmd_name)
#         cmd_parser.set_defaults(action=cmd_class)

#     for name, data in service_commands.items():
#         if name != "default" and "commands" in data:
#             for cmd_name, cmd_class in data["commands"].items():
#                 cmd_parser = subparsers.add_parser(cmd_name)
#                 cmd_parser.set_defaults(action=cmd_class)
#         if name != "default" and "groups" in data:
#             for group_name, group_data in data["groups"].items():
#                 group_parser = subparsers.add_parser(group_name)
#                 create_parsers(
#                     {
#                         "default": service_commands["default"],
#                         group_name: group_data,
#                     },
#                     group_parser,
#                 )


#     return parser
# sm/ep/desc
# test
def find_command(name, service_to_start_with, path=None):
    current_level = service_to_start_with

    # If the path is not empty, navigate through the groups
    if path:
        for part in path.split(SERVICE_PATH_SEPARATOR):
            # Find the group matching the current part of the path
            group = next(
                (
                    g
                    for g in current_level.get("groups", [])
                    if g["name"] == part
                ),
                None,
            )
            if group is None:
                return None  # Group not found
            current_level = group

    # Search for the command in the current level's commands
    command = next(
        (
            cmd
            for cmd in current_level.get("commands", [])
            if cmd["name"] == name
        ),
        None,
    )
    return command["command"] if command else None


def find_service(path, service_to_start_with):
    """Find a service by path and starting point service."""

    current_level = service_to_start_with
    for part in path.split(SERVICE_PATH_SEPARATOR):
        # Find the group matching the current part of the path
        group = next(
            (g for g in current_level.get("groups", []) if g["name"] == part),
            None,
        )
        if group is None:
            return None  # Group not found
        current_level = group
    return current_level


def handle_result(result):
    if result is False:
        sys.exit(1)
    elif result in [0, 1]:
        return result
    elif not result:
        # Handle the case where result is None, [], or {}, "", etc
        return

    command_outputs.clear()
    if isinstance(result, list):
        command_outputs.extend(result)
        if isinstance(result[0], dict):
            print_table(result)
        else:
            print_list(result)
    else:
        command_outputs.append(result)
        print_list([result])


def handle_input(user_input, path):
    input_parts = user_input.split()
    obj = find_command(
        path=path, name=input_parts[0], service_to_start_with=service_commands
    )
    # parse input_parts[1:] to dict of parameters.
    # using this format:
    # cmd param1 param2 param3=value1 param4=["value2","value3"]

    # if obj is class of type of Command
    if isinstance(obj, Command):
        # print("obj", obj)
        # print("input_parts[1:]", input_parts[1:])
        result = run_command(obj, input_parts[1:])
        handle_result(result.output)
    print(str(obj))


def main():
    register_commands([sys.modules[__name__]])
    import json

    print(json.dumps(service_commands, indent=4))
    return

    current_path = ""
    current_service = service_commands

    try:
        while True:
            prompt_symbol = (
                FontColor.GREEN_BRIGHT.value + "> " + FontColor.RESET.value
            )
            prompt = (
                f"{current_path} {prompt_symbol}"
                if current_path
                else prompt_symbol
            )
            user_input = input(prompt).strip()

            if user_input.startswith(":"):
                special_command = user_input[1:].strip()

                if special_command == "e":
                    break
                elif special_command == "ls":
                    print("Available commands:")
                    for command in current_service.get("commands", []):
                        print(f" - {command['name']}")

                    print("Available services:")
                    for group in current_service.get("groups", []):
                        print(f" - [{group['name']}]")

                elif special_command.startswith("s "):
                    path = special_command.split()[1]
                    if path == "..":
                        path = "/".join(current_path.split("/")[:-1])
                    elif path == "/":
                        path = ""

                    service = find_service(path, service_commands)
                    if service:
                        current_service = service
                        current_path = path
                    else:
                        print(f"path '{path}' is not valid.")
                else:
                    print(
                        "Unknown special command. Type ':list' to see available services or ':exit' to quit."
                    )
            else:
                # Handle action for the current service
                handle_input(user_input, current_path)
                # action = action_parts[0]
                # args = parse_args(action_parts[1:])
                # handle_action(services, current_path, action, args)
                # print(
                #     "Type ':list' to see available services or ':exit' to quit."
                # )
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")


# def main():
#     parser = create_parsers(
#         service_commands=service_commands, description="AWS AI/ML Services CLI"
#     )
#     args = parser.parse_args()

#     # Convert args to dictionary and filter out None values
#     args_dict = {k: v for k, v in vars(args).items() if v is not None}

#     if args.service and args.action:
#         # Pass the dictionary of arguments to handle_action
#         print("args_dict", args_dict)
#         return
#         handle_action(
#             service_commands,
#             args.service,
#             args.action.replace("-", "_"),
#             args_dict,
#         )
#     else:
#         parser.print_help()


if __name__ == "__main__":
    main()
