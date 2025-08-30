# Aug-25-2025
# dir_support.py

import shutil
from pathlib import Path


# Reseting directory
def reset_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if path_dir.is_dir():
        for item in path_dir.iterdir():
            if item.is_file():
                item.unlink()           # Remove file
            elif item.is_dir():
                shutil.rmtree(item)     # Remove directory
    else:
        path_dir.mkdir()


# Removing directory
def remove_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    shutil.rmtree(path_dir, ignore_errors=False, onerror=None)


# Reading the contents of a directory into a list
def read_directory_data(dir_name):

    list_data = []
    for child in dir_name.glob('*'):
        if child.is_file():

            if child.name.startswith('.'):
                continue

            list_data.append(str(child))

    return list_data


def files_number_in_directory(dir_name):

    file_count = 0
    for child in dir_name.glob('*'):
        if child.is_file():

            if child.name.startswith('.'):
                continue

            file_count += 1

    return file_count
