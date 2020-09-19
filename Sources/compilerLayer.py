from os import system, remove
from platform import system as sys
from subprocess import run


def compileAssembly(input_file: str, output_file: str):
    if system(f"gcc -m64 -c {input_file} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}"):
        return False
    remove(input_file)
    return True


def linkObjects(input_files: list, output_file: str):
    return not system(f"gcc -m64 {' '.join(input_files)} -o{output_file} {'-no-pie' if sys() == 'Linux' else ''}")


def compileJaclang(input_file: str, output_file: str, src_dir: str, proj_dir: str, obj_dir: str):
    if input_file.startswith("./"):
        input_file = input_file[2:]
    command_object = run(f"cd {proj_dir} && /usr/local/Jac/Binaries/jaclang {src_dir}/{input_file} -o{src_dir}/{output_file}.s --__dump-imports", shell=True,
                         capture_output=True)
    if command_object.returncode:
        print(command_object.stderr.decode("utf-8"), end='')
        return None
    compileAssembly(f"{proj_dir}/{src_dir}/{output_file}.s", f"{proj_dir}/{obj_dir}/{output_file}")
    return command_object.stdout.decode("utf-8").split("\n")[:-1]


def linkObjectsIntoDylib(input_files: list, output_file: str):
    return not system(f"gcc -m64 -shared -dynamiclib {' '.join(input_files)} -o{output_file}")
