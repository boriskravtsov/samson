# Aug-25-2025
# draw_canonical.py

import cv2 as cv
from pathlib import Path
from numpy import ndarray

from samson_max3.src import cfg


def draw_canonical(image: ndarray, templ: ndarray):

    canon_image_name = 'canon_' + cfg.image_name
    canon_templ_name = 'canon_' + cfg.templ_name

    path_image_canon = str(Path.cwd() / cfg.dir_debug / canon_image_name)
    path_templ_canon = str(Path.cwd() / cfg.dir_debug / canon_templ_name)

    cv.imwrite(path_image_canon, image)
    cv.imwrite(path_templ_canon, templ)
