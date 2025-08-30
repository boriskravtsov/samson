# Aug-25-2025
# tbl_scale.py

import cv2 as cv
from pathlib import Path

from tables.src import cfg_tbl
from tables.src.utils import create_empty_rgb, create_empty_grayscale


def tbl_basket_scale(list_data):

    n_shapes = len(list_data)

    tbl_empty, rows, cols = create_empty_rgb(n_shapes)

    n = 0
    for path in list_data:

        shape_scale = cv.imread(str(path), cv.IMREAD_UNCHANGED)

        nx = n % cols
        ny = n // cols

        shift_x = cfg_tbl.size_space + nx * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)
        shift_y = cfg_tbl.size_space + ny * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)

        tbl_empty[
            shift_y:shift_y + cfg_tbl.size_shape_scale,
            shift_x:shift_x + cfg_tbl.size_shape_scale] = shape_scale

        n += 1

    path_tbl = Path.cwd() / 'OUTPUT' / 'BASKET.png'
    cv.imwrite(str(path_tbl), tbl_empty)


def tbl_canonical_scale(list_data):

    n_shapes = len(list_data)

    tbl_empty, rows, cols = create_empty_grayscale(n_shapes)

    n = 0
    for path in list_data:

        shape_scale = cv.imread(str(path), cv.IMREAD_UNCHANGED)

        nx = n % cols
        ny = n // cols

        shift_x = cfg_tbl.size_space + nx * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)
        shift_y = cfg_tbl.size_space + ny * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)

        tbl_empty[
            shift_y:shift_y + cfg_tbl.size_shape_scale,
            shift_x:shift_x + cfg_tbl.size_shape_scale] = shape_scale

        n += 1

    path_tbl = Path.cwd() / 'OUTPUT' / 'BASKET_CANONICAL.png'
    cv.imwrite(str(path_tbl), tbl_empty)
