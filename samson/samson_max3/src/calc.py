# Aug-25-2025
# calc.py

import sys
import cv2 as cv
import numpy as np
from numpy import ndarray

from samson_max3.src import cfg
from samson_max3.src.magnitude import get_magn_roi, get_magn_half
from samson_max3.src.get_peaks import get_peaks
from samson_max3.src.create_table import create_table
from samson_max3.src.create_joint_table import create_joint_table
from samson_max3.src.draw_magn import draw_magn
from samson_max3.src.draw_peaks import draw_peaks
from samson_max3.src.draw_result import draw_result
from samson_max3.src.draw_image_warp import draw_image_warp
from samson_max3.src.draw_difference_map import draw_difference_map
from samson_max3.src.utils_list import save_list_of_peaks_txt


def calc(image: ndarray, templ: ndarray) -> float:

    image_flt = image.astype(np.float32)
    templ_flt = templ.astype(np.float32)

    image_magn_roi = get_magn_roi(image_flt)
    image_magn_half = get_magn_half(image_magn_roi)
    image_list_of_peaks = get_peaks(image_magn_half)

    image_table, n_image_table_rows = create_table(image_list_of_peaks)

    if n_image_table_rows == 0:
        print(f'\ncalc_similarity ERROR: ' + cfg.path_image + ' - unacceptable shape')
        sys.exit(1)

    if cfg.debug_mode:
        draw_magn('image', image_magn_roi)
        draw_peaks('image', image_list_of_peaks)
        save_list_of_peaks_txt('image_list_of_peaks', image_list_of_peaks)

    templ_magn_roi = get_magn_roi(templ_flt)
    templ_magn_half = get_magn_half(templ_magn_roi)
    templ_list_of_peaks = get_peaks(templ_magn_half)

    templ_table, n_templ_table_rows = create_table(templ_list_of_peaks)

    if n_templ_table_rows == 0:
        print(f'\ncalc_similarity ERROR: ' + cfg.path_templ + ' - unacceptable shape')
        sys.exit(1)

    if cfg.debug_mode:
        draw_magn('templ', templ_magn_roi)
        draw_peaks('templ', templ_list_of_peaks)
        save_list_of_peaks_txt('templ_list_of_peaks', templ_list_of_peaks)

    joint_table, n_joint_table_rows = \
        create_joint_table(image_table, n_image_table_rows,
                           templ_table, n_templ_table_rows)

    if n_joint_table_rows == 0:
        print(f"\nERROR: " + cfg.path_image + "  vs.  " + cfg.path_templ + " - we can't compare")
        sys.exit(1)

    distance = calc_cont(image_magn_roi, templ_magn_roi,
                         image_list_of_peaks, templ_list_of_peaks,
                         joint_table, n_joint_table_rows)

    return distance


def calc_cont(
        image_magn_roi, templ_magn_roi,
        image_list_of_peaks, templ_list_of_peaks,
        joint_table, joint_table_rows) -> (float, float):

    distance_result = np.finfo(np.float32).max
    difference_map_current = np.zeros(cfg.dsize_roi, dtype=np.float32)
    difference_map_result = np.zeros(cfg.dsize_roi, dtype=np.float32)

    for n in range(joint_table_rows):

        y_image_blue = joint_table[n, 0]
        x_image_blue = joint_table[n, 1]
        y_image_red = joint_table[n, 2]
        x_image_red = joint_table[n, 3]

        y_templ_blue = joint_table[n, 4]
        x_templ_blue = joint_table[n, 5]
        y_templ_red = joint_table[n, 6]
        x_templ_red = joint_table[n, 7]

        pts_image = np.float32([[x_image_blue, y_image_blue],
                                [x_image_red, y_image_red],
                                [cfg.X0, cfg.Y0]])

        pts_templ = np.float32([[x_templ_blue, y_templ_blue],
                                [x_templ_red, y_templ_red],
                                [cfg.X0, cfg.Y0]])

        mat_affine = cv.getAffineTransform(pts_image, pts_templ)

        image_magn_roi_warp = np.zeros_like(image_magn_roi)

        cv.warpAffine(
                image_magn_roi,
                mat_affine,
                cfg.dsize_roi,
                dst=image_magn_roi_warp,
                borderMode=cv.BORDER_TRANSPARENT)

        if cfg.debug_mode:
            distance_current, difference_map_current \
                                    = calc_cont2_map(
                                            np.float32(image_magn_roi_warp),
                                            np.float32(templ_magn_roi))
        else:
            distance_current = calc_cont2(np.float32(image_magn_roi_warp),
                                          np.float32(templ_magn_roi))

        if distance_current < distance_result:
            distance_result = distance_current

            if cfg.debug_mode:
                difference_map_result = difference_map_current.copy()

                cfg.y_image_blue = y_image_blue
                cfg.x_image_blue = x_image_blue
                cfg.y_image_red = y_image_red
                cfg.x_image_red = x_image_red

                cfg.y_templ_blue = y_templ_blue
                cfg.x_templ_blue = x_templ_blue
                cfg.y_templ_red = y_templ_red
                cfg.x_templ_red = x_templ_red

    if cfg.debug_mode:
        draw_result('image', image_list_of_peaks)
        draw_result('templ', templ_list_of_peaks)
        draw_image_warp()
        draw_difference_map(difference_map_result)

    return distance_result


def calc_cont2_map(magnitude_1: np.ndarray,
                   magnitude_2: np.ndarray):
    """
    Compute the average nonzero difference map between two magnitude arrays.

    Parameters
    ----------
    magnitude_1 : np.ndarray
        First magnitude array.
    magnitude_2 : np.ndarray
        Second magnitude array.

    Returns
    -------
    distance : float
        Average difference over nonzero pixels. Zero if no differences.
    difference_map : np.ndarray
        Element-wise difference between arrays where both are > 0.
    """

    # Ensure arrays are float32 with correct size
    arr_1 = np.maximum(magnitude_1.astype(np.float32), 0)
    arr_2 = np.maximum(magnitude_2.astype(np.float32), 0)

    # Broadcast-safe min/max
    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    # Compute difference only where arr_min > 0
    difference_map = np.where(arr_min > 0, arr_max - arr_min, 0).astype(np.float32)

    nonzero_count = float(np.count_nonzero(difference_map))

    distance = float(np.sum(difference_map) / nonzero_count) if nonzero_count > 0 else 0.0

    return distance, difference_map


def calc_cont2(magnitude_1: np.ndarray,
               magnitude_2: np.ndarray):

    arr_1 = np.maximum(magnitude_1.astype(np.float32), 0)
    arr_2 = np.maximum(magnitude_2.astype(np.float32), 0)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    difference_map = np.where(arr_min > 0, arr_max - arr_min, 0).astype(np.float32)

    nonzero_count = float(np.count_nonzero(difference_map))

    distance = float(np.sum(difference_map) / nonzero_count) if nonzero_count > 0 else 0.0

    return distance
