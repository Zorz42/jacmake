def generateMainAssembly(files_to_be_executed):
    bare_file = open("/usr/local/share/jaclang-data/entry-macho.s")
    entry_code = bare_file.read().split("\n")
    main_index = entry_code.index("_main:") + 1
    for file in reversed(files_to_be_executed):
        file = file.replace("/", "..")
        entry_code.insert(main_index, f"   call s{file}")
    return "\n".join(entry_code)

