import os
import sys
import copy
from typing import List, Tuple, Dict
from collections import deque


class Folder():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.content_folders = []
        self.content_files = []

    def add_file(self, name: str, size: int):
        self.content_files.append([name, size])

    def add_folder(self, folder):
        if folder.name == self.name:
            print('SELF_ASSIGMENT')
            return
        self.content_folders.append(folder)

    def list_folders(self):
        return self.content_folders

    def get_size(self) -> int:
        total_size = 0
        for name, size in self.content_files:
            total_size += size
        for folder in self.content_folders:
            total_size += folder.get_size()
        return total_size

    def get_parent(self):
        return self.parent

    def __str__(self) -> str:
        return f'Folder {self.name}'

    def __repr__(self) -> str:
        return self.__str__()


def cd(path_orig: str, action: str) -> str:
    if action == '/':
        return '/'
    elif action == '..':
        parts = [x+'/' for x in path_orig.split('/') if x != ''][:-1]
        result_path = ''.join(parts)
        return '/'+result_path
    else:
        return path_orig + action + '/'


def create_filepaths(filename: str) -> Dict[str, Folder]:
    root = Folder('/', None)
    files_dict: Dict[str, Folder] = {'/': root}
    path = '/'
    with open(filename, 'r') as f:
        for line in f.readlines():
            sentence = line.strip().split(' ')
            if sentence[0] == '$':
                if sentence[1] == 'cd':
                    path = cd(path, sentence[2])
                elif sentence[1] == 'ls':
                    pass
            elif sentence[0] == 'dir':
                folder_path = path+sentence[1]+'/'
                if files_dict.get(folder_path) is not None:
                    print('self_asigment')
                    continue
                new_folder = Folder(folder_path, files_dict[path])
                files_dict[path].add_folder(new_folder)
                files_dict[folder_path] = new_folder
            else:
                files_dict[path].add_file(sentence[1], int(sentence[0]))
    return files_dict


def list_folders(folder: Folder):
    subfolders = folder.list_folders()
    if subfolders:
        print(f'folder {folder} has {subfolders}')
    for sub_folder in folder.list_folders():
        list_folders(sub_folder)


def find_total_folder_space_with_less_that_n_bytes(filepaths: Dict[str, Folder], max_size: int = 100000) -> int:
    total_size = 0
    for k, v in filepaths.items():
        size = v.get_size()
        if size <= max_size:
            total_size += size
    return total_size


def find_directory_to_delete(filepaths: Dict[str, Folder], space_needed=30000000, total_space=70000000) -> Folder:
    unused_space = total_space - filepaths['/'].get_size()
    space_to_free = space_needed - unused_space
    if space_to_free < 0:
        print('No space is needed to free up')
        return Folder('', None)
    diff_list: List[Tuple[int, str]] = []
    for k, v in filepaths.items():
        size = v.get_size()
        diff = size-space_to_free
        if diff < 0:
            continue
        diff_list.append((size, k))

    diff_list.sort(key=lambda item: item[0])
    path = diff_list[0][1]
    return filepaths[path]


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    filepaths = create_filepaths(input_file)
    max_size = 100000
    total_size = find_total_folder_space_with_less_that_n_bytes(
        filepaths, max_size)
    print(
        f'Sum of the total sizes of directories with less than {max_size} is: {total_size}')

    folder = find_directory_to_delete(filepaths)
    print(
        f'the folder to delete is {folder.name} with an space of {folder.get_size()}')
