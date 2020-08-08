from os import path, mkdir, listdir
from shutil import rmtree
from platform import system as sys

from compilerLayer import compileJaclang, compileObjectsIntoDylib

object_names = []


def compileSrcDir(src_dir: str, obj_dir: str):
    for file in listdir(src_dir):
        if path.isfile(src_dir + file) and file.endswith(".jl"):
            object_names.append(f"{obj_dir}{file[:-3]}.o")
            compileJaclang(f"{src_dir}{file}", f"{obj_dir}{file[:-3]}.o")
        elif path.isdir(src_dir + file):
            mkdir(obj_dir + file)
            compileSrcDir(src_dir + file, obj_dir + file)


def compileLibrary(dir_name: str):
    if path.isdir(f"{dir_name}Objects"):
        rmtree(f"{dir_name}Objects")
    mkdir(f"{dir_name}Objects")
    compileSrcDir(f"{dir_name}Sources/", f"{dir_name}Objects/")
    if object_names:
        compileObjectsIntoDylib(object_names, f"{dir_name}/lib.{'so' if sys() == 'Linux' else 'dylib'}")
    rmtree(f"{dir_name}Objects/")


def compileDir(dir_name: str):
    if not dir_name[-1] == "/":
        dir_name += "/"
    if path.isfile(f"{dir_name}Info.json") and path.isdir(f"{dir_name}Sources"):
        compileLibrary(dir_name)
    else:
        print(f"Warning: skipping {dir_name} as it is not recognized as anything or has already been compiled.")


def compileDirs(dirs_to_compile: list):
    for dir_name in dirs_to_compile:
        compileDir(dir_name)
