# Aug-25-2025
# draw_magn.py

import sys
import os
import cv2 as cv
import numpy as np
from numpy import ndarray

from samson_max3.src import cfg


def draw_magn(tag, any_image_magn: ndarray):

    any_image_magn = any_image_magn.astype(np.uint8)

    # Save Magnitude in file as grayscale.
    # ---------------------------------------------------------
    magnitude_gray_path = cfg.dir_debug + '/' + tag + '_gray.png'
    result = cv.imwrite(magnitude_gray_path, any_image_magn)

    if result is False:
        print('ERROR: draw_magn()')
        sys.exit(1)
    # ---------------------------------------------------------

    # Convert Magnitude to ColorMap.
    # ---------------------------------------------------------
    magnitude_color = np.uint8(0)

    if os.path.exists(magnitude_gray_path):

        magnitude_gray = cv.imread(magnitude_gray_path, cv.IMREAD_GRAYSCALE)

        os.remove(magnitude_gray_path)

        if cfg.colormap == 'HOT':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_HOT)

        if cfg.colormap == 'HSV':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_HSV)

        if cfg.colormap == 'JET':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_JET)

        if cfg.colormap == 'TURBO':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_TURBO)
    else:
        print("ERROR in draw_magn(): The file does not exist")
        sys.exit(1)
    # ---------------------------------------------------------

    magnitude_color_path = cfg.dir_debug + '/' + tag + '.png'
    cv.imwrite(magnitude_color_path, magnitude_color)
