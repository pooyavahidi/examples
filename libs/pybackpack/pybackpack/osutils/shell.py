import os
import subprocess
from pybackpack.commands import Command, CommandResult


# pylint: disable=too-many-arguments,too-many-instance-attributes
class ProcessCommand(Command):
    """This class is a wrapper around subprocess.run() to run shell commands.

    The result of the command is stored in the `result` attribute. Also the
    stdout of the command is returned by the `run()` method.
    Attributes:
        cmd (list): The command to run.
        capture_output (bool): Capture stdout and stderr.
        check (bool): If True, raise an exception if the command fails.
        text (bool): If True, stdout and stderr are returned as strings.
        timeout (int): The timeout for the command.
        cwd (str): The current working directory.
        shell (bool): If True, run the command in a shell.
        encoding (str): The encoding of the command output.
        errors (str): The error handling of the command output.
        stdin (int): The stdin of the command.
        input_data (str): The input for the command.
        env (dict): The environment variables for the command.
        inherit_env (bool): If True, use the current environment as the base.
        other_popen_kwargs (dict): Keyword arguments for subprocess.Popen.
    """

    def __init__(
        self,
        cmd,
        capture_output=True,
        check=True,
        text=True,
        encoding="utf-8",
        timeout=None,
        cwd=None,
        shell=False,
        errors=None,
        stdin=None,
        input_data=None,
        env=None,
        inherit_env=True,
        raise_error=False,
        **other_popen_kwargs,
    ):
        super().__init__(input_data=input_data, raise_error=raise_error)

        if inherit_env:
            # Use the current environment as the base
            self.env = os.environ.copy()
            if env:
                # Update with provided env variables
                self.env.update(env)
        else:
            self.env = env

        self.cmd = cmd
        self.capture_output = capture_output
        self.check = check
        self.text = text
        self.timeout = timeout
        self.cwd = cwd
        self.shell = shell
        self.encoding = encoding
        self.errors = errors
        self.stdin = stdin
        self.other_popen_kwargs = other_popen_kwargs

        # Failed flags
        self.failed_with_time_out = False
        self.failed_with_command_not_found = False

    def _run(self) -> CommandResult:
        try:
            result = subprocess.run(
                self.cmd,
                capture_output=self.capture_output,
                check=self.check,
                text=self.text,
                timeout=self.timeout,
                cwd=self.cwd,
                env=self.env,
                shell=self.shell,
                encoding=self.encoding,
                errors=self.errors,
                stdin=self.stdin,
                input=self.input_data,
                **self.other_popen_kwargs,
            )
            return CommandResult(
                output=result.stdout,
                metadata=result,
            )

        except Exception as e:  # pylint: disable=broad-except
            if isinstance(e, subprocess.TimeoutExpired):
                self.failed_with_time_out = True
            if isinstance(e, FileNotFoundError):
                self.failed_with_command_not_found = True

            raise e
