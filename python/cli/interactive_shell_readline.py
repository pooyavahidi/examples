import readline
from abc import ABC, abstractmethod

# Note: In order to enable vi mode in MacOS (which by default uses libedit),
# either add `bind -v` in the `.editrc` file or uncomment the following:
#readline.parse_and_bind('bind -v')


class bcolors:
    FAIL = "\033[91m"
    RESET = "\033[0m"


class command(ABC):
    def __init__(self, params):
        self._params = params

    @abstractmethod
    def _execute(self):
        pass

    def execute(self):
        return self._execute()


class printer(command):
    def _execute(self):
        return print(self._params)


def command_builder(cmd_str):
    cmd_parts = cmd_str.split(" ", 1)
    if cmd_parts[0] == "print":
        return printer(cmd_parts[1])


def main():
    while True:
        cmd_str = input(">>> ")

        if cmd_str == "exit":
            break

        try:
            cmd = command_builder(cmd_str)
            if not cmd:
                raise Exception("Not supported")

            cmd.execute()
        except Exception as e:
            print(bcolors.FAIL + str(e) + bcolors.RESET)


if __name__ == "__main__":
    main()
