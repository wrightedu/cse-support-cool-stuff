#!/usr/bin/env python

from genericpath import isdir
import os
from os import path

ROOT_DIR = './'

def print_directory(dir_path, index_file, recursion_level=0):
    print(f'Found the directory {dir_path}')

    # TODO These custom names mean that things can get out of alphebetical order
    if path.exists(path.join(dir_path, 'name.txt')):
        with open(path.join(dir_path, 'name.txt'), 'r') as f:
            print('    found custom name')
            name = f.read()
    else:
        name = path.split(dir_path)[-1].replace('-', ' ').title()

    short_path = path.join(dir_path, 'short.md')
    index_path = path.join(dir_path, 'index.md') if path.exists(path.join(dir_path, 'index.md')) else path.join(dir_path, 'readme.md')

    index_file.write(f'\n{"#" * (recursion_level + 2)} {name}\n\n')

    if path.exists(short_path) and path.isfile(short_path):
        print('    short description found')
        with open(short_path, 'r') as f:
            index_file.write(f.read())
        index_file.write('\n')
    else:
        print('    no short description found')
        index_file.write('_(no description available)_\n')

    if path.exists(index_path) and path.isfile(index_path):
        print('    additional info found')
        index_file.write(f'\n[read more]({index_path})\n')

    # TODO maybe do some detection of code here?

    for i in sorted(os.listdir(dir_path)):
        full_path = path.join(dir_path, i)

        if path.isdir(full_path):
            print_directory(full_path, index_file, recursion_level + 1)

    

if __name__ == '__main__':
    # TODO Add a sanity check that this is being run as part of a GitHub action
    with open(path.join(ROOT_DIR, 'index.md'), 'w') as f:
        with open(path.join(ROOT_DIR, 'index.head.md'), 'r') as header:
            f.write(header.read())

        for i in sorted(os.listdir(ROOT_DIR)):
            full_path = path.join(ROOT_DIR, i)

            if path.isdir(full_path):
                print_directory(full_path, f)


        with open(path.join(ROOT_DIR, 'index.tail.md'), 'r') as footer:
            f.write(footer.read())