# Aug-25-2025
# get_canon_shapes_distance.py

import sys
import cv2 as cv

from samson_max3.src.calc import calc


def get_canon_shapes_distance(path_image: str, path_templ: str) -> float:

    image_gray = cv.imread(path_image, cv.IMREAD_UNCHANGED)
    if image_gray is None:
        print(f'\nERROR: Unable to read {path_image}.')
        sys.exit(1)

    templ_gray = cv.imread(path_templ, cv.IMREAD_UNCHANGED)
    if templ_gray is None:
        print(f'\nERROR: Unable to read {path_templ}.')
        sys.exit(1)

    distance_1 = calc(image_gray, templ_gray)
    distance_2 = calc(templ_gray, image_gray)

    return min(distance_1, distance_2)
