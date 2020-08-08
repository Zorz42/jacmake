from os import system, remove
from platform import system as sys
from subprocess import run, PIPE


def compileAssembly(input_file: str, output_file: str):
    system(f"gcc -c {input_file} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")
    remove(input_file)


def linkObjects(input_files: list, output_file: str):
    system(f"gcc {' '.join(input_files)} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")


def compileJaclang(input_file: str, output_file: str):
    command_object = run(f"/usr/local/Jac/Binaries/jaclang {input_file} -o{output_file}.s --__dump-imports", shell=True, stdout=PIPE)
    if command_object.returncode:
        exit(1)
    compileAssembly(f"{output_file}.s", output_file)
    return command_object.stdout.decode("utf-8").split("\n")[:-1]


def compileObjectsIntoDylib(input_files: list, output_file: str):
    system(f"gcc -dynamiclib {' '.join(input_files)} -o{output_file}")
