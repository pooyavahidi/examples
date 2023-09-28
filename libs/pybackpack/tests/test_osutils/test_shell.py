import pytest
from pybackpack.osutils.shell import ProcessCommand
from pybackpack.commands import (
    PipeCommand,
    SequentialCommand,
)


def setup_files_and_dirs(tmpdir):
    tmpdir.mkdir("dir1")
    return tmpdir


def test_shell_command():
    cmd = ProcessCommand(["echo", "Hello"])
    res = cmd.run()
    assert res.output == "Hello\n"
    assert res.metadata.returncode == 0

    # Access result from cmd object
    assert cmd.result.metadata.returncode == 0
    assert cmd.result.metadata.stdout == "Hello\n"

    # Test with env variables
    cmd = ProcessCommand(["env"], env={"MY_VAR": "test1"})
    res = cmd.run()
    assert "MY_VAR=test1" in res.output

    # Test long running command
    cmd = ProcessCommand(["sleep", "2"], timeout=1)
    res = cmd.run()
    assert res.output is None
    assert res.succeeded is False
    assert cmd.failed_with_time_out is True

    # Test failed command
    cmd = ProcessCommand(["ls", "unknown"])
    res = cmd.run()
    assert res.output is None
    assert res.succeeded is False
    assert res.error.returncode == 2
    assert "No such file or directory" in res.error.stderr

    # Test failed command with ignore_errors=False. It will raise an exception
    cmd = ProcessCommand(["ls", "unknown"], raise_error=True)
    with pytest.raises(Exception):
        cmd.run()
    assert cmd.result.succeeded is False
    assert cmd.result.error.returncode == 2

    # Test failed with command not found
    cmd = ProcessCommand(["unknown"])
    res = cmd.run()
    assert res.output is None
    assert res.error.errno == 2
    assert cmd.failed_with_command_not_found is True
    assert "No such file or directory" in res.error.strerror

    # Multiline output
    cmd = ProcessCommand(["ls", "/", "-l"])
    res = cmd.run()
    assert res.output is not None
    assert len(res.output.splitlines()) > 1


def test_pipe():
    # Pipe commands
    commands = [
        ProcessCommand(["echo", "Hello World"]),
        ProcessCommand(["cut", "-d", " ", "-f", "1"]),
        ProcessCommand(["awk", "{print $1}"]),
    ]
    pipe = PipeCommand(commands)
    res = pipe.run()
    assert res.succeeded is True
    assert res.output == "Hello\n"
    assert pipe.commands[0].result.metadata.returncode == 0
    assert pipe.commands[0].result.metadata.stdout == "Hello World\n"
    assert pipe.commands[1].result.metadata.returncode == 0
    assert pipe.commands[2].result.metadata.returncode == 0

    # Test with a failing command in the middle
    commands = [
        ProcessCommand(["echo", "Hello World"]),
        ProcessCommand(["cut", "-d", " ", "-f", "1"]),
        ProcessCommand(["unknown"]),
        ProcessCommand(["awk", "{print $1}"]),
    ]
    pipe = PipeCommand(commands)
    res = pipe.run()
    assert res.output is None
    assert res.succeeded is False
    assert pipe.commands[0].result.succeeded is True
    assert pipe.commands[0].result.output == "Hello World\n"
    assert pipe.commands[1].result.succeeded is True
    assert pipe.commands[1].result.output == "Hello\n"
    assert pipe.commands[2].result.succeeded is False
    assert pipe.commands[2].result.output is None
    assert pipe.commands[3].result is None


def test_pipe_permission_error(tmpdir):
    d = setup_files_and_dirs(tmpdir)
    d.chmod(0o000)

    commands = [
        ProcessCommand(["echo", "Hello World"]),
        ProcessCommand(["ls", d]),
    ]
    pipe = PipeCommand(commands)
    res = pipe.run()
    assert res.output is None
    assert res.succeeded is False
    assert pipe.commands[0].result.succeeded is True
    assert pipe.commands[0].result.output == "Hello World\n"
    assert pipe.commands[1].result.succeeded is False
    assert pipe.commands[1].result.output is None
    assert pipe.commands[1].result.error.returncode == 2
    assert "Permission denied" in pipe.commands[1].result.error.stderr


def test_sequential():
    # Simulate && operator in shell
    commands = [
        ProcessCommand(["echo", "Hello"]),
        ProcessCommand(["echo", "World"]),
    ]
    seq = SequentialCommand(commands)
    res = seq.run()
    assert {"Hello\n", "World\n"} == set(res.output)

    # Simulate && with error
    commands = [
        ProcessCommand(["echo", "Hello"]),
        ProcessCommand(["ls", "unknown"]),
        ProcessCommand(["echo", "World"]),
    ]
    seq = SequentialCommand(commands)
    res = seq.run()
    assert ["Hello\n", None] == res.output
    assert res.succeeded is False
    # resul of the first command
    assert seq.commands[0].result.metadata.returncode == 0
    assert seq.commands[0].result.metadata.stdout == "Hello\n"
    # The command which failed
    assert seq.commands[1].result.succeeded is False
    assert seq.commands[1].result.error.returncode == 2
    assert "No such file or directory" in seq.commands[1].result.error.stderr

    # Simulate || operator in shell
    commands = [
        ProcessCommand(["echo", "Hello"]),
        ProcessCommand(["ls", "unknown"]),
        ProcessCommand(["echo", "World"]),
    ]
    seq = SequentialCommand(commands, operator="||")
    result = seq.run()
    assert result.output == ["Hello\n"]

    # Simulatte ; operator in shell
    commands = [
        ProcessCommand(["echo", "Hello"]),
        ProcessCommand(["ls", "unknown"]),
        ProcessCommand(["echo", "World"]),
    ]
    seq = SequentialCommand(commands, operator=None)
    result = seq.run()
    assert ["Hello\n", None, "World\n"] == result.output

    # Invalid operator
    with pytest.raises(ValueError):
        SequentialCommand(commands, operator="invalid").run()


def test_sequential_combined():
    # Sequential combined
    cmd1 = SequentialCommand(
        [
            ProcessCommand(["echo", "1"]),
            ProcessCommand(["python3", "-c", "import os; print(os.getpid())"]),
        ]
    )
    cmd2 = SequentialCommand(
        [
            ProcessCommand(["echo", "2"]),
            ProcessCommand(["python3", "-c", "import os; print(os.getpid())"]),
        ]
    )
    cmd3 = SequentialCommand(
        [
            ProcessCommand(["echo", "3"]),
            ProcessCommand(["python3", "-c", "import os; print(os.getpid())"]),
        ]
    )

    # Run the commands in sequence
    seq = SequentialCommand([cmd1, cmd2, cmd3])
    result = seq.run()
    assert len(result.output) == 3
