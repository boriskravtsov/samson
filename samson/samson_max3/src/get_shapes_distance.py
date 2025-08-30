# Aug-25-2025
# get_shapes_distance.py

import sys
import cv2 as cv

from samson_max3.src import cfg
from samson_max3.src.to_canonical import to_canonical_2
from samson_max3.src.calc import calc
from samson_max3.src.draw_canonical import draw_canonical


def get_shapes_distance(path_image: str, path_templ: str) -> float:

    image_gray = cv.imread(path_image, cv.IMREAD_GRAYSCALE)
    if image_gray is None:
        print(f'\nERROR: Unable to read {path_image}.')
        sys.exit(1)

    templ_gray = cv.imread(path_templ, cv.IMREAD_GRAYSCALE)
    if templ_gray is None:
        print(f'\nERROR: Unable to read {path_templ}.')
        sys.exit(1)

    image_canon = to_canonical_2(image_gray)
    templ_canon = to_canonical_2(templ_gray)

    if cfg.debug_mode:
        draw_canonical(image_canon, templ_canon)

    distance_1 = calc(image_canon, templ_canon)
    distance_2 = calc(templ_canon, image_canon)

    return min(distance_1, distance_2)
