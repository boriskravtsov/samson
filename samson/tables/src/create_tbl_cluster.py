# Aug-25-2025
# create_tbl_cluster.py

import os
import cv2 as cv
from pathlib import Path

from tables.src import cfg_tbl
from tables.src.utils import create_empty_rgb


def create_tbl_cluster(cluster_number):

    path_cluster_number = Path.cwd() / 'CLUSTERS' / str(cluster_number)

    n_shapes = len([f for f in os.listdir(path_cluster_number)])
    # print(f"\nNumber of shapes: {n_shapes}")

    tbl_empty, rows, cols = create_empty_rgb(n_shapes)

    png_files = list(path_cluster_number.glob("*.png"))

    n = 0
    for shape_path in png_files:

        shape_name = os.path.basename(shape_path)
        shape_path = Path.cwd() / '_TEMP' / 'BASKET_SCALE' / shape_name

        shape_scale = cv.imread(str(shape_path), cv.IMREAD_UNCHANGED)

        nx = n % cols
        ny = n // cols

        shift_x = cfg_tbl.size_space + nx * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)
        shift_y = cfg_tbl.size_space + ny * (cfg_tbl.size_space + cfg_tbl.size_shape_scale)

        tbl_empty[
            shift_y:shift_y + cfg_tbl.size_shape_scale,
            shift_x:shift_x + cfg_tbl.size_shape_scale] = shape_scale

        n += 1

    cluster_n = 'CLUSTER_' + str(cluster_number) + '.png'
    path_cluster_out = Path.cwd() / 'OUTPUT' / cluster_n
    cv.imwrite(str(path_cluster_out), tbl_empty)
