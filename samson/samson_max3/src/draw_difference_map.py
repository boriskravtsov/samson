# Aug-25-2025
# draw_difference_map.py

import sys
import os
import cv2 as cv
import numpy as np
from numpy import ndarray

from samson_max3.src import cfg


def draw_difference_map(difference_map: ndarray):

    difference_map_norm = np.zeros(cfg.dsize_roi, dtype=np.float32)

    cv.normalize(difference_map, difference_map_norm, 0, 255, cv.NORM_MINMAX)

    difference_map_view = difference_map_norm.astype(np.uint8)

    # Save difference_map in file as grayscale.
    # ---------------------------------------------------------
    difference_map_gray_path = cfg.dir_debug + '/' + 'difference_map_gray.png'
    result = cv.imwrite(difference_map_gray_path, difference_map_view)

    if result is False:
        print('ERROR: draw_difference_map()')
        sys.exit(1)
    # ---------------------------------------------------------

    # Convert difference_map to ColorMap.
    # ---------------------------------------------------------
    if os.path.exists(difference_map_gray_path):

        difference_map_gray = cv.imread(difference_map_gray_path, cv.IMREAD_GRAYSCALE)

        difference_map_color = cv.applyColorMap(difference_map_gray, cv.COLORMAP_HOT)
    else:
        print("ERROR in draw_difference_map(): The file does not exist")
        sys.exit(1)
    # ---------------------------------------------------------

    difference_map_color_path = cfg.dir_debug + '/' + 'difference_map.png'
    cv.imwrite(difference_map_color_path, difference_map_color)
