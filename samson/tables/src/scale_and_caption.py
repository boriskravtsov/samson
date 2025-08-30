# Aug-25-2025
# scale_and_caption.py

import os
import cv2 as cv
from pathlib import Path

from tables.src import cfg_tbl
from utils.src.dir_support import read_directory_data, remove_directory


def basket_scale_and_caption(dir_basket_scale):
    """
    Читаем изображения из директории BASKET_24bpp, масштабируем,
    добавляем заголоки и сохраняем в директории _TEMP/BASKET_SCALE.
    """
    dir_basket_24bpp = Path.cwd() / 'BASKET_24bpp'
    list_basket_filepaths = read_directory_data(dir_basket_24bpp)

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (0, 0, 0)
    thickness = 1
    text_position = (5, 23)

    for path in list_basket_filepaths:

        shape = cv.imread(str(path), cv.IMREAD_COLOR_BGR)

        shape_scale \
            = cv.resize(shape, cfg_tbl.size_scale, cv.INTER_LANCZOS4)

        shape_name = os.path.basename(path)
        caption = shape_name.removesuffix('.png')

        if cfg_tbl.text_flag:
            cv.putText(shape_scale,
                       caption,
                       text_position,
                       font,
                       font_scale,
                       font_color,
                       thickness,
                       cv.LINE_AA)

        path_out = dir_basket_scale / shape_name
        cv.imwrite(str(path_out), shape_scale)

    remove_directory(dir_basket_24bpp)


def canonical_scale(dir_basket_canon_scale):
    """
    Читаем изображения из директории CANONICAL, масштабируем
    и сохраняем в директории _TEMP/CANONICAL_SCALE.
    """
    dir_canonical = Path.cwd() / 'CANONICAL'
    list_canonical_filepaths = read_directory_data(dir_canonical)

    for path in list_canonical_filepaths:

        shape = cv.imread(str(path), cv.IMREAD_UNCHANGED)

        shape_scale \
            = cv.resize(shape, cfg_tbl.size_scale, cv.INTER_LANCZOS4)

        shape_name = os.path.basename(path)

        path_out = dir_basket_canon_scale / shape_name
        cv.imwrite(str(path_out), shape_scale)
