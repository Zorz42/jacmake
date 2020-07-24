from platform import system as sys


def generateMainAssembly(files_to_be_executed):
    if sys() == "Linux":
        osplatform = "linux"
    elif sys() == "Darwin":
        osplatform = "OSX"
    else:
        print("Unsupported platform!")
        exit(1)

    bare_file = open(f"/usr/local/share/jaclang-data/entry-{'gnu' if osplatform == 'Linux' else 'macho'}.s")
    entry_code = bare_file.read().split("\n")
    main_index = entry_code.index("_main:") + 1
    for file in reversed(files_to_be_executed):
        file = file.replace("/", "..")
        entry_code.insert(main_index, f"   call s{file}")
    return "\n".join(entry_code)
