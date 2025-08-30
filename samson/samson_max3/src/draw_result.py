# Aug-25-2025
# draw_result.py

import cv2 as cv

from samson_max3.src import cfg
from samson_max3.src.draw_utils import draw_peak, draw_text


def draw_result(tag, list_of_peaks):

    path_in = cfg.dir_debug + '/' + tag + '.png'
    magn = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    x3: int = cfg.X0
    y3: int = cfg.Y0

    if tag == 'image':
        x1 = cfg.x_image_red
        y1 = cfg.y_image_red
        x2 = cfg.x_image_blue
        y2 = cfg.y_image_blue

    if tag == 'templ':
        x1 = cfg.x_templ_red
        y1 = cfg.y_templ_red
        x2 = cfg.x_templ_blue
        y2 = cfg.y_templ_blue

    # Draw lines
    # -----------------------------------------
    thickness = 2

    cv.line(magn,
            (x1, y1),
            (x2, y2),
            cfg.clover, thickness)  # green

    cv.line(magn,
            (x1, y1),
            (x3, y3),
            cfg.maraschino, thickness)  # red

    cv.line(magn,
            (x2, y2),
            (x3, y3),
            cfg.aqua, thickness)  # blue
    # -----------------------------------------

    # Draw peaks
    # -----------------------------------------
    n = 0
    for item in list_of_peaks:
        y = int(item[0])
        x = int(item[1])
        draw_peak(magn, x, y, cfg.dark_gray, 2, -1)
        if n > 0:
            draw_text(magn, x + 5, y + 0, cfg.black, str(n))
        else:
            draw_text(magn, x - 7, y + 23, cfg.black, str(n))
        n += 1
    # -----------------------------------------

    path_out = cfg.dir_debug + '/' + tag + '_result.png'
    cv.imwrite(path_out, magn)
