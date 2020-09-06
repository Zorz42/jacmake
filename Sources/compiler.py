from os import path, mkdir, listdir
from shutil import rmtree
from platform import system as sys
from json import load, JSONDecodeError

from compilerLayer import compileJaclang, linkObjectsIntoDylib, linkObjects, compileAssembly
from entryGenerator import generateEntry

info_json, object_names = {}, []


def compileSrcDir(src_dir: str, obj_dir: str):
    for file in listdir(src_dir):
        if path.isfile(src_dir + file) and file.endswith(".jl"):
            object_names.append(f"{obj_dir}{file[:-3]}.o")
            if not path.isfile(f"{obj_dir}{file[:-3]}.o") or \
                    path.getmtime(src_dir + file) > path.getmtime(f"{obj_dir}{file[:-3]}.o"):
                if file == "__entry.jl":
                    print("File cannot be named \"__entry.jl\"")
                    return False
                if compileJaclang(src_dir + file, f"{obj_dir}{file[:-3]}.o") is None:
                    return False
        elif path.isdir(src_dir + file):
            mkdir(obj_dir + file)
            if not compileSrcDir(src_dir + file, obj_dir + file):
                return False
    return True


def compileLibrary(dir_name: str):
    if path.isdir(f"{dir_name}Objects"):
        rmtree(f"{dir_name}Objects")
    mkdir(f"{dir_name}Objects")
    if not compileSrcDir(f"{dir_name}Sources/", f"{dir_name}Objects/"):
        print("Compilation failed!")
        return
    if object_names:
        if not linkObjectsIntoDylib(object_names, f"{dir_name}lib.{'so' if sys() == 'Linux' else 'dylib'}"):
            print("Compilation failed!")
            return
    rmtree(f"{dir_name}Objects")


def compileProgram(dir_name: str, exec_name: str, files_to_execute: list):
    if not path.isdir(f"{dir_name}Objects"):
        mkdir(f"{dir_name}Objects")

    if not compileSrcDir(f"{dir_name}Sources/", f"{dir_name}Objects/"):
        print("Compilation failed!")
        return
    files_to_execute = [dir_name + file for file in files_to_execute]
    with open(f"{dir_name}Objects/__entry.s", "w") as entry_file:
        entry_file.write(generateEntry(files_to_execute))
    compileAssembly(f"{dir_name}Objects/__entry.s", f"{dir_name}Objects/__entry.o")
    object_names.append(f"{dir_name}Objects/__entry.o")

    if not linkObjects(object_names, exec_name):
        print("Compilation failed!")
        return


def compileDir(dir_name: str):
    if not dir_name[-1] == "/":
        dir_name += "/"

    if not path.isdir(dir_name):
        print(f"Warning: skipping {dir_name} as it does not exist.")
        return

    if not path.isfile(f"{dir_name}Info.json"):
        print(f"Warning: skipping {dir_name} as it is not recognized as anything.")
        return
    if not path.isdir(f"{dir_name}Sources"):
        print(f"Warning: skipping {dir_name} as it is not valid.")
        return

    with open(f"{dir_name}Info.json") as file:
        try:
            global info_json
            info_json = load(file)
        except JSONDecodeError:
            print(f"Warning: skipping {dir_name} as it does not have a valid json file.")
            return
    if "Type" in info_json:
        if info_json["Type"] == "Package" or info_json["Type"] == "Dependency":
            compileLibrary(dir_name)
        elif info_json["Type"] == "Program":
            if "ExecName" in info_json and "StartFiles" in info_json:
                for file in info_json["StartFiles"]:
                    if not path.isfile(f"{dir_name}/{file}"):
                        print(f"Starter file {file} does not exist!")
                        return
                compileProgram(dir_name, info_json["ExecName"], info_json["StartFiles"])
            else:
                print(f"Warning: skipping {dir_name} as it does not have a valid info file.")
        else:
            print(f"Warning: skipping {dir_name} as it is not recognized as anything.")
    else:
        print(f"Warning: skipping {dir_name} as it does not have a valid info file.")


def compileDirs(dirs: list):
    for dir_name in dirs:
        compileDir(dir_name)
