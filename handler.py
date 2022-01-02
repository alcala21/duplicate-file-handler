import sys
import os
import textwrap
from collections import defaultdict


def get_sorting():
    print(textwrap.dedent("""
    Size sorting options:
    1. Descending
    2. Ascending
    """))

    _sorting = 0
    while True:
        try:
            _sorting = int(input("Enter sorting option:\n"))
            if _sorting <= 2:
                break
            else:
                print()
                print("Wrong option", end="\n\n")
        except ValueError:
            pass

    return _sorting


try:
    root = sys.argv[1]
    file_format = input("Enter file format:\n")
    sorting = get_sorting()
    duplicates = defaultdict(list)
    for sub_root, folders, files in os.walk(root):
        for file in files:
            if file.split('.')[-1] == file_format or not file_format:
                fullname = os.path.join(sub_root, file)
                size = os.path.getsize(fullname)
                duplicates[size].append(fullname)
    sorted_sizes = sorted(duplicates, reverse=(sorting == 1))
    for size in sorted_sizes:
        print(size, 'bytes')
        for file in duplicates[size]:
            print(file)
        print()

except IndexError:
    print("Directory is not specified")
