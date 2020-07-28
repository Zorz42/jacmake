from sys import version_info, argv
from os import remove
from platform import system as sys

from entryGenerator import generateEntry
from compilerLayer import compileJaclang, compileAssembly, linkObjects

version = "1.1.0"
arguments = argv[1:]
object_names = []


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

    for file in arguments:
        print(f"Compiling {file}")
        if not file.endswith(".jl"):
            print("Unknown file extension!")
            exit(0)
        if file == "__entry.jl":
            print("File cannot be named \"__entry.jl\"")
            exit(0)

        file_name = ".".join(file.split(".")[:-1])

        compileJaclang(file_name)
        object_names.append(f"{file_name}.o")

    print("Generating entry")
    entry_file_path_prefix = "/".join(object_names[0].split("/")[:-1])
    entry_file_path = entry_file_path_prefix + ("/" if entry_file_path_prefix else "") + "__entry"
    with open(f"{entry_file_path}.s", "w") as entry_file:
        entry_file.write(generateEntry([arguments[0]]))

    compileAssembly(entry_file_path)

    object_names.append(f"{entry_file_path}.o")

    print("Linking files")
    linkObjects(object_names, object_names[0][:-2])

    for object_file in object_names:
        remove(object_file)


if __name__ == '__main__':
    main()

