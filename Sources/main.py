from sys import version_info, argv
from os import path
from platform import system as sys

from fileCompiler import compileFiles
from dirCompiler import compileDirs

version = "1.2.1"
arguments = argv[1:]


def main():
    if version_info.major != 3:
        print("Must be using python3!")
        exit(1)

    if sys() != "Linux" and sys() != "Darwin":
        print("Unsupported platform!")
        exit(1)

    if not arguments:
        print(f"Jacmake {version} - help")
        with open("/usr/local/Jac/Data/jacmake-help.txt") as help_file:
            print(help_file.read(), end='')
        exit(0)

    compileDirs([file for file in arguments if path.isdir(file)])
    compileFiles([file for file in arguments if path.isfile(file)])


if __name__ == '__main__':
    main()

