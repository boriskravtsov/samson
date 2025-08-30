# Aug-25-2025
# utils.py

import numpy as np

from tables.src import cfg_tbl


# Вычисление количества рядов (rows) и столбцов (cols) таблицы
def tbl_dimension(n_shapes: int) -> (int, int):

    if n_shapes <= cfg_tbl.cols_max:
        rows = 1
        cols = n_shapes
    else:
        cols = cfg_tbl.cols_max

        temp1 = n_shapes // cols
        temp2 = n_shapes % cols

        if temp2 == 0:
            rows = temp1
        else:
            rows = temp1 + 1

    return rows, cols


"""
Создание пустого rgb-изображения под будущую таблицу с формами.

Размер изображения tbl_empty определяется количеством 
изображений и нашим выбором cfg_tbl.cols_max = 8 (максимальным 
числом столбцов в таблице).
"""
def create_empty_rgb(n_shapes):

    rows, cols = tbl_dimension(n_shapes)

    tbl_base_width = cols * cfg_tbl.size_shape_scale + (cols + 1) * cfg_tbl.size_space
    tbl_base_height = rows * cfg_tbl.size_shape_scale + (rows + 1) * cfg_tbl.size_space

    tbl_empty = np.empty((tbl_base_height, tbl_base_width, 3), dtype=np.uint8)

    tbl_empty.fill(cfg_tbl.color_background)

    return tbl_empty, rows, cols


"""
Создание пустого grayscale-изображения под будущую таблицу с формами.

Размер изображения tbl_empty определяется количеством 
изображений и нашим выбором cfg_tbl.cols_max = 8 (максимальным 
числом столбцов в таблице).
"""
def create_empty_grayscale(n_shapes):

    rows, cols = tbl_dimension(n_shapes)

    tbl_base_width = cols * cfg_tbl.size_shape_scale + (cols + 1) * cfg_tbl.size_space
    tbl_base_height = rows * cfg_tbl.size_shape_scale + (rows + 1) * cfg_tbl.size_space

    tbl_empty = np.empty((tbl_base_height, tbl_base_width), dtype=np.uint8)

    tbl_empty.fill(cfg_tbl.color_background)

    return tbl_empty, rows, cols
