# Aug-25-2025
# draw_peaks.py

import cv2 as cv

from samson_max3.src import cfg
from samson_max3.src.draw_utils import draw_peak, draw_text


def draw_peaks(tag, list_of_peaks):

    path_in = cfg.dir_debug + '/' + tag + '.png'
    magn = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    # Draw peaks
    # -----------------------------------------
    n = 0
    for item in list_of_peaks:
        y = int(item[0])
        x = int(item[1])
        draw_peak(magn, x, y, cfg.black, 2, -1)
        if n > 0:
            draw_text(magn, x + 5, y + 0, cfg.black, str(n))
        else:
            draw_text(magn, x - 7, y + 23, cfg.black, str(n))
        n += 1
    # -----------------------------------------

    path_out = cfg.dir_debug + '/' + tag + '_peaks.png'
    cv.imwrite(path_out, magn)
