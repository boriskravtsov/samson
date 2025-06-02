# Jun-02-2025
# distances.py

import os
import cv2 as cv
import numpy as np
from pathlib import Path
from tqdm import tqdm

from max3 import to_canonical_1
from max3.src.get_canon_shapes_distance import get_canon_shapes_distance
from utils.src.dir_support import reset_directory, read_directory_data
from utils.src.timer import init_timer, save_elapsed_time_hour_min_sec


def distances(dir_basket):

    init_timer()

    dir_canonical = Path.cwd() / 'CANONICAL'
    dir_output = Path.cwd() / 'OUTPUT'
    reset_directory(dir_canonical)
    reset_directory(dir_output)

    convert_to_rgb(dir_basket)

    list_basket_paths = read_directory_data(dir_basket)
    n_shapes = len(list_basket_paths)

    # Изображения из директории BASKET преобразуем в канонический вид -
    # grayscale, [100 x 100] pixels и помещаем в директорию CANONICAL.
    to_canonical_1(dir_canonical, list_basket_paths)
    list_canonical_paths = read_directory_data(dir_canonical)
    list_canonical_paths.sort()

    D = np.zeros((n_shapes, n_shapes), dtype=np.float32)

    n_shapes_x = n_shapes * n_shapes
    list_indexes = []
    for n in range(n_shapes_x):

        j = n // n_shapes
        i = n % n_shapes

        if i <= j:
            continue

        list_indexes.append((j, i))

    n_calc = len(list_indexes)

    print()
    for n in tqdm(range(n_calc), desc='distances'):

        temp = list_indexes[n]

        j = temp[0]
        i = temp[1]

        path_j = list_canonical_paths[j]
        path_i = list_canonical_paths[i]

        distance = get_canon_shapes_distance(path_i, path_j)

        D[j, i] = distance
        D[i, j] = distance

    path_time = Path.cwd() / 'OUTPUT' / 'time.txt'
    save_elapsed_time_hour_min_sec(path_time)

    return D


def convert_to_rgb(input_dir):

    # Process each file in the directory
    for filename in os.listdir(input_dir):

        if filename.startswith('.'):
            continue

        file_path = os.path.join(input_dir, filename)

        # Read the image without changing the format
        img = cv.imread(file_path, cv.IMREAD_UNCHANGED)

        # Check if image is grayscale
        if img is not None:
            if len(img.shape) == 2:
                # Grayscale image has shape (H, W), convert to RGB
                rgb_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
                cv.imwrite(file_path, rgb_img)
            else:
                """ Already RGB or non-grayscale """
        else:
            print(f"Failed to load image: {filename}")
