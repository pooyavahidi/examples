import os
import pytest
from pybackpack.commands import (
    Command,
    CommandResult,
    SequentialCommand,
    ParallelCommand,
    PipeCommand,
)


class AddCharCommand(Command):
    def __init__(self, char=None) -> None:
        super().__init__()
        self.char = char

    def _run(self):
        if not self.input_data:
            self.input_data = ""
        return CommandResult(f"{self.input_data}{self.char}")


class ErrorCommand(Command):
    def __init__(self, raise_error=False) -> None:
        super().__init__(raise_error=raise_error)
        self.error_message = "Error from ErrorCommand"

    def _run(self):
        if self.raise_error:
            raise SystemError(self.error_message)

        return CommandResult(
            output=None,
            succeeded=False,
            error_message=self.error_message,
        )


class ErrorAlwaysRaiseCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    def _run(self):
        raise SystemError("Error from ErrorAlwaysRaiseCommand")


class ProcessInfoCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    def _run(self):
        return CommandResult(output=os.getpid())


def test_single_command():
    cmd = AddCharCommand("A")
    result = cmd.run()
    assert result.output == "A"
    assert result.succeeded is True

    # Command with error
    cmd = ErrorCommand(raise_error=True)
    with pytest.raises(SystemError):
        cmd.run()
    assert cmd.result.succeeded is False
    assert cmd.result.output is None
    assert isinstance(cmd.result.error, SystemError)
    assert cmd.result.error_message == "Error from ErrorCommand"

    # Command with error and raise_error=False
    cmd = ErrorCommand(raise_error=False)
    result = cmd.run()
    assert result.output is None
    assert result.succeeded is False
    assert result.error_message == "Error from ErrorCommand"

    # Test always raising error command.
    # Even it raises error internally, since raise_error=False,
    # it should not raise error.
    cmd = ErrorAlwaysRaiseCommand()
    cmd.run()
    assert cmd.result.succeeded is False
    assert cmd.result.output is None
    assert isinstance(cmd.result.error, SystemError)

    # Test always raising error command with raise_error=True
    cmd = ErrorAlwaysRaiseCommand()
    cmd.raise_error = True
    with pytest.raises(SystemError):
        cmd.run()
    assert cmd.result.succeeded is False
    assert cmd.result.output is None
    assert isinstance(cmd.result.error, SystemError)


def test_pipe():
    commands = [
        AddCharCommand("A"),
        AddCharCommand("B"),
        AddCharCommand("C"),
    ]
    pipe = PipeCommand(commands)
    result = pipe.run()
    assert result.output == "ABC"

    # Test pipe with initial input
    commands = [
        AddCharCommand("A"),
        AddCharCommand("B"),
        AddCharCommand("C"),
    ]
    pipe = PipeCommand(commands)
    result = pipe.run("D")
    assert result.output == "DABC"
    assert pipe.commands[0].result.output == "DA"
    assert pipe.commands[0].result.succeeded is True
    assert pipe.commands[1].result.output == "DAB"
    assert pipe.commands[2].result.output == "DABC"

    # Test pipe with error
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
    ]
    pipe = PipeCommand(commands)
    result = pipe.run()
    assert result.output is None
    assert result.succeeded is False
    assert result.error_message == "Error from ErrorCommand"

    # Test pipe without raising error with a command that always raises error
    # Note: Pipe doesn't raise error even if one of the commands raises error.
    commands = [
        AddCharCommand("A"),
        ErrorAlwaysRaiseCommand(),
        AddCharCommand("C"),
    ]
    pipe = PipeCommand(commands)
    result = pipe.run()
    assert result.succeeded is False
    assert result.output is None
    assert isinstance(result.error, SystemError)

    # Test pipe with error and raise_error=True. It forces all commands to
    # raise error if applicable.
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
    ]
    pipe = PipeCommand(commands, raise_error=True)
    with pytest.raises(SystemError):
        pipe.run()
    assert pipe.result.succeeded is False
    assert pipe.result.output is None
    assert pipe.result.error_message == "Error from ErrorCommand"
    assert isinstance(pipe.result.error, SystemError)
    assert pipe.commands[0].result.output == "A"
    assert isinstance(pipe.commands[1].result.error, SystemError)


def test_sequential():
    # Simulate && in unix-like shell
    commands = [
        AddCharCommand("A"),
        AddCharCommand("B"),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands)
    result = seq.run()
    assert result.output == ["A", "B", "C"]
    assert result.succeeded is True

    # Simulate && in unix-like shell with error
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands)
    result = seq.run()
    assert result.output == ["A", None]
    assert result.succeeded is False

    # Simulate || in unix-like shell
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands, operator="||")
    result = seq.run()
    assert result.output == ["A"]

    # Simulate || in unix-like shell with error early
    commands = [
        ErrorCommand(raise_error=False),
        ErrorCommand(raise_error=False),
        AddCharCommand("A"),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands, operator="||")
    result = seq.run()
    assert result.output == [None, None, "A"]
    assert result.succeeded is True

    # Simulate || in unix-like shell without error
    commands = [
        AddCharCommand("A"),
        AddCharCommand("B"),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands, operator="||")
    result = seq.run()
    assert result.output == ["A"]
    assert result.succeeded is True

    # Simulate || without collecting outputs
    commands = [
        ErrorCommand(raise_error=False),
        AddCharCommand("A"),
        AddCharCommand("C"),
    ]
    seq = SequentialCommand(commands, operator="||", collect_outputs=False)
    result = seq.run()
    assert result.output is None
    assert result.succeeded is True
    assert seq.commands[0].result.output is None
    assert seq.commands[1].result.output == "A"
    assert seq.commands[2].result is None

    # Simulate ; in unix-like shell
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
        ErrorAlwaysRaiseCommand(),
        AddCharCommand("B"),
        ErrorCommand(raise_error=True),
    ]
    seq = SequentialCommand(commands, operator=None)
    result = seq.run()
    assert [cmd.result.succeeded for cmd in seq.commands] == [
        True,
        False,
        True,
        False,
        True,
        False,
    ]
    assert result.output == ["A", None, "C", None, "B", None]
    # Command which did not raised error, the succeded is False but there is no
    # error.
    assert seq.commands[1].result.succeeded is False
    assert seq.commands[1].result.error is None
    assert isinstance(seq.commands[3].result.error, SystemError)
    assert seq.commands[5].result.succeeded is False
    assert seq.commands[5].result.error is None

    # Simulate ; in unix-like shell with error when raise_error=True
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
        ErrorAlwaysRaiseCommand(),
        AddCharCommand("B"),
        ErrorCommand(raise_error=True),
    ]
    seq = SequentialCommand(commands, operator=None, raise_error=True)
    result = seq.run()
    assert result.output == ["A", None, "C", None, "B", None]


def test_sequential_combined():
    cmd1 = SequentialCommand([AddCharCommand("A"), AddCharCommand("B")])
    cmd2 = SequentialCommand([AddCharCommand("C"), AddCharCommand("D")])
    seq = SequentialCommand([cmd1, cmd2])
    result = seq.run()
    assert result.output == [["A", "B"], ["C", "D"]]
    assert result.succeeded is True
    assert seq.commands[0].result.output == ["A", "B"]
    assert seq.commands[1].commands[0].result.output == "C"

    # Combined using process info
    seq = SequentialCommand(
        [ProcessInfoCommand(), ProcessInfoCommand(), ProcessInfoCommand()]
    )
    result = seq.run()
    assert result.succeeded is True
    # Process Ids should be identical since both are run in the same process
    assert result.output[0] == result.output[1] == result.output[2]


def test_parallel():
    # Run Parallel commands without error
    commands = [
        AddCharCommand("A"),
        AddCharCommand("B"),
        AddCharCommand("C"),
    ]
    par = ParallelCommand(commands)
    result = par.run()
    assert result.output == ["A", "B", "C"]
    assert result.succeeded is True

    # Run Parallel commands with error
    commands = [
        AddCharCommand("A"),
        ErrorCommand(raise_error=False),
        AddCharCommand("C"),
        ErrorAlwaysRaiseCommand(),
        AddCharCommand("B"),
        ErrorCommand(raise_error=True),
    ]
    par = ParallelCommand(commands)
    result = par.run()
    assert result.succeeded is True
    assert result.output == ["A", None, "C", None, "B", None]

    # Combined using process info
    seq = ParallelCommand(
        [ProcessInfoCommand(), ProcessInfoCommand(), ProcessInfoCommand()]
    )
    result = seq.run()
    assert result.succeeded is True
    # Process Ids are different since they are run in different processes
    # The following doesn't pass in the vscode debug mode as it doesn't
    # spawn a new process for each command in the Pool.
    # Run the test using pytest in the terminal to see the correct result.
    assert result.output[0] != result.output[1] != result.output[2]
