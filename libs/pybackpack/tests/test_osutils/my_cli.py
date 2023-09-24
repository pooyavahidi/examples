#!/usr/bin/env python3

import sys
import pathlib
import subprocess

# import the pybackpack by adding it to the path.
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from pybackpack.osutils.cli import (
    ParserComposite,
    CliRunner,
    cli_handler,
)


runner = CliRunner()


class RootComposite(ParserComposite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._add_sub_parsers(help="sub-command level 1 (command group) help")

        self.parser.add_argument(
            "--version", dest="version", action="store_true"
        )
        DeployerComposite(
            "deployer",
            self,
            help="this is the deployer command group",
        )
        ShowComposite("show", self)
        NoHandlerComposite("nohandler", self)


class NoHandlerComposite(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)


class DeployerComposite(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)

        self._add_sub_parsers(help="sub-command level 2 (command group) help")

        LogsParser(
            "logs",
            self,
            help="logs help",
        )


class ShowComposite(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)

        self._add_sub_parsers(
            help="sub-command level 2 (command) help",
        )

        ShowArgsParser("args", self)
        DirParser("dir", self)


class DirParser(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)


class LogsParser(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)

        self.parser.add_argument(
            "-v", "--verbose", dest="verbose", action="store_true"
        )

        self.parser.add_argument(
            "-l",
            "--limit",
            help="Returns the specified number of events",
            dest="logs_limit",
        )


class ShowArgsParser(ParserComposite):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)


@cli_handler(runner=runner)
def default_handler(version, **kwargs):
    if version:
        print("v0.0.0")
        return
    return False


@cli_handler(runner=runner, commands=["show", "dir"])
def show_dir_handler(props, **kwargs):
    print(props["directory"])
    subprocess.run(["ls", props["directory"]], check=True)


@cli_handler(runner=runner, commands=["show", "args"])
def show_args_handler(**kwargs):
    print("test")


@cli_handler(runner=runner, commands=["deployer", "logs"])
def deployer_logs_handler(logs_limit, verbose, **kwargs):
    if logs_limit:
        if logs_limit == "0":
            raise Exception("Error!")
        else:
            print(logs_limit)
            return
    if verbose:
        print("deployer logs verbose")
        return
    return False


if __name__ == "__main__":
    # Create root parser composite and parse the arguments
    root = RootComposite(description="sample of multi level commands")

    props = {"directory": "/tmp"}
    runner.run(root.parser, props)  # , ["--version", "deployer", "logs"])
