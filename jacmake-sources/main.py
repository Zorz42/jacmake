from sys import argv
from os import system, remove
from mainAssemblyGenerator import generateMainAssembly

arguments = argv[1:]
object_names = []

if not arguments:
    print("No input files!")
    exit(0)

for file in arguments:
    print(f"Compiling {file}")
    file_name = file.split(".")
    file_name.pop()
    file_name = ".".join(file_name)

    system(f"jaclang {file} -o{file_name}.s --quiet")
    system(f"gcc -c {file_name}.s -o{file_name}.o")
    remove(f"{file_name}.s")
    object_names.append(f"{file_name}.o")

print("Generating entry")
entry_file_path_prefix = "/".join(object_names[0].split("/")[:-1])
entry_file_path = entry_file_path_prefix + ("/" if entry_file_path_prefix else "") + "__entry.s"
entry_file = open(entry_file_path, "w")
entry_file.write(generateMainAssembly([arguments[0]]))
entry_file.close()
system(f"gcc -c {entry_file_path} -o{entry_file_path[:-2]}.o")

object_names.append(f"{entry_file_path[:-2]}.o")

print("Linking files")
system(f"gcc {' '.join(object_names)} -o{object_names[0][:-2]}")

for object_file in object_names:
    remove(object_file)
