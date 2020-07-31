from os import system, remove
from platform import system as sys


def compileAssembly(input_file: str, output_file: str):
    system(f"gcc -c {input_file}.s -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")
    remove(output_file)


def linkObjects(input_files: list, output_file: str):
    system(f"gcc {' '.join(input_files)} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")


def compileJaclang(input_file: str, output_file: str):
    system(f"jaclang {input_file} -o{output_file}.s --quiet")
    compileAssembly(f"{output_file}.s", output_file)
