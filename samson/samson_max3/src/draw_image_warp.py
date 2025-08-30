# Aug-25-2025
# draw_image_warp.py

import cv2 as cv
import numpy as np
from pathlib import Path

from samson_max3.src import cfg


def draw_image_warp():

    path_in = str(Path.cwd() / cfg.dir_debug / 'image.png')
    image_in = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    y_image_blue = cfg.y_image_blue
    x_image_blue = cfg.x_image_blue
    y_image_red = cfg.y_image_red
    x_image_red = cfg.x_image_red

    y_templ_blue = cfg.y_templ_blue
    x_templ_blue = cfg.x_templ_blue
    y_templ_red = cfg.y_templ_red
    x_templ_red = cfg.x_templ_red

    pts_image = np.float32([[x_image_blue, y_image_blue],
                            [x_image_red, y_image_red],
                            [cfg.X0, cfg.Y0]])

    pts_templ = np.float32([[x_templ_blue, y_templ_blue],
                            [x_templ_red, y_templ_red],
                            [cfg.X0, cfg.Y0]])

    mat_affine = cv.getAffineTransform(pts_image, pts_templ)

    image_out = np.zeros_like(image_in)

    cv.warpAffine(
        image_in,
        mat_affine,
        cfg.dsize_roi,
        dst=image_out,
        borderMode=cv.BORDER_TRANSPARENT)

    path_out = str(Path.cwd() / cfg.dir_debug / 'image_warp.png')
    cv.imwrite(path_out, image_out)
