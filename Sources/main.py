#!/usr/bin/env python3

from sys import version_info, argv, path as import_path
from platform import system as sys

import_path.append("/usr/local/Jac/Jacmake")

from compiler import compileDirs
from creator import createDirs

version = "1.4.1"
arguments = argv[1:]


def main():
    if version_info.major != 3:
        print("Must be using python3!")
        exit(1)

    if sys() != "Linux" and sys() != "Darwin":
        print("Unsupported platform!")
        exit(1)

    next_to_create, to_compile, to_create = False, [], []
    for argument in arguments:
        if next_to_create:
            to_create.append(argument)
            next_to_create = False
        else:
            if argument == "--create":
                next_to_create = True
            else:
                to_compile.append(argument)

    if not arguments:
        print(f"Jacmake {version} - help")
        with open("/usr/local/Jac/Data/jacmake-help.txt") as help_file:
            print(help_file.read(), end='')
    else:
        createDirs(to_create)
        compileDirs(to_compile)


if __name__ == '__main__':
    main()
