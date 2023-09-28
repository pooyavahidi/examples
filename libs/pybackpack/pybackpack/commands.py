from typing import Any, List, Optional, Dict
from multiprocessing import Pool, cpu_count
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class CommandResult:
    """Represents the result of a command execution.

    Attributes:
        output: The output of the command.
        succeeded: A boolean indicating whether the command was successful.
        error: The exception raised by the command if it failed.
        error_message: The error message if the command failed.
        metadata: A dictionary containing any additional metadata.
    """

    output: Any
    succeeded: bool = True
    error: Any = None
    error_message: str = None
    metadata: Any = None


class Command(ABC):
    """
    An abstract class for any class that can be run.

    Provides a common interface for all classes which implement
    the `Command` pattern.

    Attributes:
        input_data: The input provided for the command.
        result: The result after executing the command.
        raise_error: A boolean indicating whether to raise an error if any
            command fails. Defaults to False.
    """

    def __init__(self, input_data: Optional[Any] = None, raise_error=False):
        self.input_data = input_data
        self.result: Optional[CommandResult] = None
        self.raise_error = raise_error

    def run(self, input_data: Optional[Any] = None) -> CommandResult:
        """Runs the command.

        If `input_data` is provided, it sets the command input,
        and then calls the _run method to execute.

        Args:
            input_data: The input for the command. Defaults to None.

        Returns:
            CommandResult: The result after executing the command.
        """

        if input_data is not None:
            self.input_data = input_data
        try:
            self.result = self._run()
        except Exception as e:  # pylint: disable=broad-except
            self.result = CommandResult(
                output=None,
                succeeded=False,
                error=e,
                error_message=str(e),
            )
            if self.raise_error:
                raise e

        return self.result

    @abstractmethod
    def _run(self) -> CommandResult:
        """Executes the command and returns a CommandResult."""
        raise NotImplementedError


class PipeCommand(Command):
    """
    This is a Macro Command which runs the commands in sequence, similar to a
    shell's pipe. The output of each command is provided as input to the next
    command in sequence. If any command fails, the pipeline stops and returns
    the result with success set to False. An error is raised if no commands
    list is provided.

    Attributes:
        commands: A list of Command objects to be executed in sequence.
        input_data: Initial input for the first command. Defaults to None.
        raise_error: A boolean indicating whether to raise an error if any
            command fails. Defaults to False.
    """

    def __init__(
        self,
        commands: List[Command],
        input_data: Any = None,
        raise_error=False,
    ):
        super().__init__(input_data=input_data, raise_error=raise_error)

        if commands is None:
            raise ValueError("Commands list cannot be None")

        self.commands = commands

    def _run(self) -> CommandResult:
        # The first command starts with the input_data provided to the pipe.
        output = self.input_data
        for command in self.commands:
            # Set the raise_error attribute of each command to the parent
            # command's raise_error attribute.
            command.raise_error = self.raise_error

            result = command.run(input_data=output)

            if not result.succeeded:
                return result

            output = result.output

        return CommandResult(output=output)


class SequentialCommand(Command):
    """This is a Macro Command which runs the commands sequentially with an
    option to set the operator between the commands.

    Each command runs after the previous command has finished in the sequence.
    The `operator` attribute sets the operation between the commands. This
    attribute is similar to the `&&`, `||` and `;` operators in Unix-like
    shells.

    Attributes:
        commands: A list of Command objects to be executed in sequence.
        operator: The operator between the commands. Defaults to `&&`.
            - If the operator is `&&` (default), then the next command will
            run only if the previous command was successful.
            - If the operator is `||`, then the next command will run only if
            the previous command failed.
            - If the operator is None, it will act like the `;` operator,
            meaning the next command will run regardless of the outcome of the
            previous command.
        collect_outputs: A boolean indicating whether to collect the outputs
            of all commands. Defaults to True.
        raise_error: A boolean indicating whether to raise an error if any
            command fails. Defaults to False.
    """

    def __init__(
        self,
        commands: List[Command],
        operator="&&",
        collect_outputs=True,
        raise_error=False,
    ):
        super().__init__(raise_error=raise_error)
        # Validations
        if commands is None:
            raise ValueError("Commands list cannot be None")
        if operator not in ["&&", "||", None]:
            raise ValueError("Invalid operator")

        self.commands = commands
        self.operator = operator
        self.collect_outputs = collect_outputs

    def _run(self) -> CommandResult:
        outputs = []
        result = None

        for command in self.commands:
            try:
                # Set the raise_error attribute of each command to the parent
                # command's raise_error attribute.
                command.raise_error = self.raise_error

                result = command.run()

                if self.collect_outputs:
                    outputs.append(result.output)

                if not result.succeeded and self.operator == "&&":
                    break

                if result.succeeded and self.operator == "||":
                    break

            except Exception:  # pylint: disable=broad-except
                if self.collect_outputs:
                    outputs.append(None)

                if self.operator == "&&":
                    break
                if self.operator == "||":
                    continue

        return CommandResult(
            output=outputs if self.collect_outputs else None,
            succeeded=result.succeeded if result else False,
        )


def execute_command(command: Command) -> CommandResult:
    """Function to execute a given command.

    Args:
        command: A Command object to execute.

    Returns:
        CommandResult: The result after executing the command.
    """
    return command.run()


class ParallelCommand(Command):
    """This is a Macro Command which runs the commands in parallel using
    multiprocessing.

    The commands are indepndent of each other and can be run in parallel. This
    class uses the `multiprocessing.Pool` to run the commands in parallel.

    Attributes:
        commands: A list of Command objects to be executed in parallel.
        number_of_processes: The number of processes to be used to run the
            commands. Defaults to the number of CPUs available on the system.
        collect_outputs: A boolean indicating whether to collect the outputs
            of all commands. Defaults to True.
        raise_error: A boolean indicating whether to raise an error if any
            command fails. Defaults to False.
    """

    def __init__(
        self,
        commands: List[Command],
        number_of_processes: int = None,
        collect_outputs=True,
        raise_error=False,
    ):
        super().__init__(raise_error=raise_error)
        if commands is None:
            raise ValueError("Commands list cannot be None")

        self.commands = commands
        self.collect_outputs = collect_outputs
        self.pool_size = number_of_processes or cpu_count()

    def _run(self) -> CommandResult:
        outputs = None

        # Set the raise_error attribute of each command to the parent
        # command's raise_error attribute.
        for command in self.commands:
            command.raise_error = self.raise_error

        with Pool(self.pool_size) as pool:
            results = pool.map(execute_command, self.commands)

        # Update each command's result attribute with the returned results.
        # This is because using multiprocessing, each command is run in a
        # separate process. Each process has its own memory space. Thus, any
        # change to the command object inside the child process (like setting
        # the result attribute) will not be reflected in the command object of
        # the parent process.
        for i, command in enumerate(self.commands):
            command.result = results[i]

        # If collect_outputs is True, gather outputs of all results.
        if self.collect_outputs:
            outputs = [result.output for result in results if result]

        return CommandResult(output=outputs)
