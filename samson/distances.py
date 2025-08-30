# Aug-25-2025
# distances.py

import os
import cv2 as cv
import numpy as np
from pathlib import Path
from tqdm import tqdm

from samson_max3.src.to_canonical import to_canonical_1
from samson_max3.src.get_canon_shapes_distance import get_canon_shapes_distance
from utils.src.dir_support import reset_directory, read_directory_data
from utils.src.timer import init_timer, save_elapsed_time_hour_min_sec


def distances(dir_basket):

    init_timer()

    dir_basket_24bpp = Path.cwd() / 'BASKET_24bpp'
    dir_canonical = Path.cwd() / 'CANONICAL'
    dir_output = Path.cwd() / 'OUTPUT'
    reset_directory(dir_basket_24bpp)
    reset_directory(dir_canonical)
    reset_directory(dir_output)

    convert_to_rgb24bpp(dir_basket, dir_basket_24bpp)

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


def convert_to_rgb24bpp(input_dir, output_dir):

    # Process each file in the directory
    for filename in os.listdir(input_dir):

        if filename.startswith('.'):
            continue

        file_path_in = os.path.join(input_dir, filename)
        file_path_out = os.path.join(output_dir, filename)

        # Read the image without changing the format
        img = cv.imread(file_path_in, cv.IMREAD_UNCHANGED)

        if img is not None:

            num_channels = get_image_channels(file_path_in)

            if num_channels == 1:
                rgb_img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
                cv.imwrite(file_path_out, rgb_img)

            if num_channels == 3:
                cv.imwrite(file_path_out, img)

            if num_channels == 4:
                rgb_img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)
                cv.imwrite(file_path_out, rgb_img)

        else:
            print(f"Failed to load image: {filename}")


def get_image_channels(image_path):
    """
    Loads an image and returns its number of channels.

    Args:
        image_path (str): The path to the image file.

    Returns:
        int or None: The number of channels if the image is loaded successfully,
                     None otherwise.
    """

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return None

    # Load the image
    # cv2.imread returns a NumPy array.
    # For color images (BGR), it will be (height, width, 3).
    # For grayscale images, it will be (height, width).
    image = cv.imread(image_path, cv.IMREAD_UNCHANGED)  # Use IMREAD_UNCHANGED to read image as is, including alpha channel

    if image is None:
        print(f"Error: Could not load image from '{image_path}'. Check file format or corruption.")
        return None

    # Get the shape of the image array
    # The shape attribute returns a tuple: (height, width, channels) for color images,
    # and (height, width) for grayscale images.
    image_shape = image.shape

    # Determine the number of channels based on the shape's length
    if len(image_shape) == 3:
        # If the shape has 3 dimensions, it's a color image.
        # The third element of the shape tuple is the number of channels.
        num_channels = image_shape[2]
        """
        print(f"The image '{os.path.basename(image_path)}' has {num_channels} channels.")
        if num_channels == 3:
            print("This is likely a standard BGR/RGB color image.")
        elif num_channels == 4:
            print("This is likely a BGR/RGB image with an alpha (transparency) channel.")
        """
    elif len(image_shape) == 2:
        # If the shape has 2 dimensions, it's a grayscale image.
        # Grayscale images have 1 channel.
        num_channels = 1
        # print(f"The image '{os.path.basename(image_path)}' has {num_channels} channel (grayscale).")
    else:
        # This case is highly unlikely for typical images but included for robustness.
        num_channels = None
        # print(f"The image '{os.path.basename(image_path)}' has an unexpected number of dimensions: {len(image_shape)}")

    return num_channels
