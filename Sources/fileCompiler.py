from os import remove, path
from platform import system as sys

from entryGenerator import generateEntry
from compilerLayer import compileJaclang, compileAssembly, linkObjects


def compileFiles(files_to_compile: list):
    object_names, libraries_to_link = [], []
    if not files_to_compile:
        return
    for file in files_to_compile:
        print(f"Compiling {file}")
        if not file.endswith(".jl"):
            print("Unknown file extension!")
            exit(0)
        if file == "__entry.jl":
            print("File cannot be named \"__entry.jl\"")
            exit(0)

        file_name = ".".join(file.split(".")[:-1])

        libraries_to_link += compileJaclang(f"{file_name}.jl", f"{file_name}.o")
        object_names.append(f"{file_name}.o")

    print("Generating entry")
    entry_file_path_prefix = "/".join(object_names[0].split("/")[:-1])
    entry_file_path = entry_file_path_prefix + ("/" if entry_file_path_prefix else "") + "__entry"
    with open(f"{entry_file_path}.s", "w") as entry_file:
        entry_file.write(generateEntry([files_to_compile[0]]))

    compileAssembly(f"{entry_file_path}.s", f"{entry_file_path}.o")

    object_names.append(f"{entry_file_path}.o")

    libraries_to_link = [f"/usr/local/Jac/Libraries/{library}/lib.{'so' if sys() == 'Linux' else 'dylib'}" for library
                         in libraries_to_link if
                         path.isfile(f"/usr/local/Jac/Libraries/{library}/lib.{'so' if sys() == 'Linux' else 'dylib'}")]

    print("Linking files")
    linkObjects(object_names + libraries_to_link, object_names[0][:-2])

    for object_file in object_names:
        remove(object_file)
