from os import path
from shutil import rmtree


def compileDir(dir_name: str):
    if not dir_name[-1] == "/":
        dir_name += "/"
    if not path.isfile(f"{dir_name}Info.json") or not path.isdir(f"{dir_name}Sources"):
        print(f"Warning: skipping {dir_name} as it is not recognized as anything.")
        return
    if path.isdir(f"{dir_name}Objects"):
        rmtree(f"{dir_name}Objects")
    
    print(dir_name)


def compileDirs(dirs_to_compile: list):
    for dir_name in dirs_to_compile:
        compileDir(dir_name)
