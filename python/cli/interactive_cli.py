import readline
from abc import ABC, abstractmethod


class bcolors:
    FAIL = "\033[91m"
    ENDC = "\033[0m"


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
    match cmd_str.split():
        case ["print", *obj]:
            return printer(obj)


def main():
    while True:
        cmd_str = input(">>> ")

        if cmd_str == "quit":
            break

        try:
            cmd = command_builder(cmd_str)
            if not cmd:
                raise Exception("Not supported")

            cmd.execute()
        except Exception as e:
            print(bcolors.FAIL + str(e) + bcolors.ENDC)


if __name__ == "__main__":
    main()
