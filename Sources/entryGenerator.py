from platform import system as sys
from re import compile as re_compile

def generateEntry(files_to_be_executed: list):
    bare_file = open(f"/usr/local/Jac/Data/entry-{'gnu' if sys() == 'Linux' else 'macho'}.s")
    entry_code = bare_file.read().split("\n")
    main_index = entry_code.index('main:' if sys() == 'Linux' else '_main:') + 1
    regex = re_compile('[^a-zA-Z/]')
    for file in reversed(files_to_be_executed):
        file = regex.sub('', file)
        file = file.replace("/", ".")
        entry_code.insert(main_index, f"   call s{file}")
    return "\n".join(entry_code)

