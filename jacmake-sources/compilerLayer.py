from os import system, remove
from platform import system as sys


def compileAssembly(file_name: str):
    system(f"gcc -c {file_name}.s -o{file_name}.o {'-no-pie' if sys() == 'Linux' else ''}")
    remove(f"{file_name}.s")


def linkObjects(object_files: list, output_file: str):
    system(f"gcc {' '.join(object_files)} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")


def compileJaclang(file_name: str):
    system(f"jaclang {file_name}.jl -o{file_name}.s --quiet")
    compileAssembly(file_name)
