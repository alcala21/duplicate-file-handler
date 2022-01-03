import sys
import os
import textwrap
from collections import defaultdict
import hashlib


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


def ask_question(_message):
    while True:
        answer = input(f"{_message}\n")
        if answer.lower() == 'yes':
            return True
        elif answer.lower() == 'no':
            return False
        else:
            print("\nWrong option\n")


def get_hashvalue(_file):
    buffer_size = 65536
    md5 = hashlib.md5()
    with open(_file, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def find_duplicates(_sizes, _files):
    _hashvalues = dict()
    for _size in _sizes:
        _hashvalues[_size] = defaultdict(list)
        for _file in _files[_size]:
            _hashvalues[_size][get_hashvalue(_file)].append(_file)
        for _hashvalue in _hashvalues[_size].copy():
            if len(_hashvalues[_size][_hashvalue]) == 1:
                del _hashvalues[_size][_hashvalue]
    for _size in _sizes:
        if len(_hashvalues[_size]) == 0:
            del _hashvalues[_size]
    return _hashvalues


def get_indices(length):
    length_list = list(range(length))
    while True:
        try:
            _indices = [int(x) for x in input("Enter file numbers to delete:\n").split()]
            _indices[0]
            for _index in _indices:
                length_list[_index - 1]
            else:
                return _indices
        except (ValueError, IndexError):
            print("\nWrong format\n")


try:
    root = sys.argv[1]
    file_format = input("Enter file format:\n")
    sorting = get_sorting()
    duplicates = defaultdict(list)
    for sub_root, folders, files in os.walk(root):
        for _file in files:
            if _file.split('.')[-1] == file_format or not file_format:
                fullname = os.path.join(sub_root, _file)
                size = os.path.getsize(fullname)
                duplicates[size].append(fullname)
    sorted_sizes = sorted(duplicates, reverse=(sorting == 1))
    for size in sorted_sizes:
        print(size, 'bytes')
        for _file in duplicates[size]:
            print(_file)
        print()

    if ask_question("Check for duplicates?"):
        hashvalues = find_duplicates(sorted_sizes, duplicates)
        count = 1
        print()
        duplicate_list = list()
        for size in hashvalues:
            print(size, 'bytes')
            for hashvalue in hashvalues[size]:
                files = hashvalues[size][hashvalue]
                print('Hash:', hashvalue)
                for _file in files:
                    print(f"{count}.", _file)
                    duplicate_list.append(_file)
                    count += 1
            print()

        if ask_question("Delete files?"):
            indices = get_indices(len(duplicate_list))
            freedsize = 0
            for index in indices:
                freedsize += os.path.getsize(duplicate_list[index - 1])
                os.remove(duplicate_list[index - 1])
            print(f"Total freed up space: {freedsize} bytes")

except IndexError:
    print("Directory is not specified")
