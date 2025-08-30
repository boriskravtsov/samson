# Aug-25-2025
# file_support.py

import os


def get_filenames_from_filepaths(list_filepaths):

    list_filenames = []
    for item in list_filepaths:
        filename = os.path.basename(item)
        list_filenames.append(filename)

    return list_filenames
