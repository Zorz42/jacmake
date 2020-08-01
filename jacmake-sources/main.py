from sys import version_info, argv
from os import path
from platform import system as sys

from fileCompiler import compileFiles
from dirCompiler import compileDirs

version = "1.1.1"
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
        print("jacmake [input files/directories]... - compile files into one executable, you can also compile:")
        print("     - jaclang packages/libraries (automatically called by jpm)")
        print("     - jaclang projects (coming soon...)")
        exit(0)

    compileDirs([file for file in arguments if path.isdir(file)])
    compileFiles([file for file in arguments if path.isfile(file)])


if __name__ == '__main__':
    main()

