from os import path, mkdir
from json import dump


def createDir(dir_name: str):
    if path.isdir(dir_name):
        print(f"{dir_name} already exists!")
        return
    print(f"Creating {dir_name}")
    mkdir(dir_name)

    sub_dirs = ("Sources", "Headers")
    for sub_dir in sub_dirs:
        mkdir(f"{dir_name}/{sub_dir}")

    # create main file
    open(f"{dir_name}/Sources/main.jl", "a").close()

    parent_dirs = dir_name.split("/")
    while parent_dirs[-1] == "":
        parent_dirs.pop()

    info = {
        "Type": "Program",
        "ExecName": parent_dirs[-1],
        "StartFiles": ["Sources/main.jl"],
    }

    with open(f"{dir_name}/Info.json", "w") as info_file:
        dump(info, info_file, indent=4)


def createDirs(dirs: list):
    for dir_name in dirs:
        createDir(dir_name)