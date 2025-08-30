# Aug-25-2025
# get_tabular_results.py

from pathlib import Path
import random

from tables.src.tbl_scale import tbl_basket_scale, tbl_canonical_scale
from tables.src.scale_and_caption import basket_scale_and_caption, canonical_scale
from tables.src.create_tbl_cluster import create_tbl_cluster
from utils.src.dir_support import reset_directory, read_directory_data, remove_directory


def get_tabular_results():

    dir_temp = Path.cwd() / '_TEMP'
    dir_basket_scale = Path.cwd() / '_TEMP' / 'BASKET_SCALE'
    dir_canonical_scale = Path.cwd() / '_TEMP' / 'CANONICAL_SCALE'
    reset_directory(dir_temp)
    reset_directory(dir_basket_scale)
    reset_directory(dir_canonical_scale)

    dir_clusters = Path.cwd() / 'CLUSTERS'

    """
    Читаем формы из директории BASKET, масштабируем в [166 x 166] для 
    показа в таблице, добавляем заголовки (опция) и сохраняем в директории 
    _TEMP/BASKET_SCALE.
    """
    basket_scale_and_caption(dir_basket_scale)

    """
    Читаем формы из директории CANONICAL, масштабируем в [166 x 166] 
    для показа в таблице и сохраняем в директории _TEMP/CANONICAL_SCALE.
    """
    canonical_scale(dir_canonical_scale)

    # BASKET_SCALE
    # -------------------------------------------------------------
    list_paths = read_directory_data(dir_basket_scale)
    n_shapes = len(list_paths)
    indexes = list(range(n_shapes))
    random.shuffle(indexes)

    list_paths_random = []
    for n in range(n_shapes):
        index = indexes[n]
        list_paths_random.append(list_paths[index])

    tbl_basket_scale(list_paths_random)
    # -------------------------------------------------------------

    # CANONICAL_SCALE
    # -------------------------------------------------------------
    list_paths = read_directory_data(dir_canonical_scale)

    list_paths_random = []
    for n in range(n_shapes):
        index = indexes[n]
        list_paths_random.append(list_paths[index])

    tbl_canonical_scale(list_paths_random)
    # -------------------------------------------------------------

    # Визуализация содержимого всех кластеров
    # -------------------------------------------------------------
    folders = [f.name for f in dir_clusters.iterdir() if f.is_dir()]

    for item in folders:
        create_tbl_cluster(int(item))
    # -------------------------------------------------------------

    # Clean up
    # -------------------------------------------------------------
    dir_canonical = Path.cwd() / 'CANONICAL'
    remove_directory(dir_canonical)
    remove_directory(dir_clusters)
    remove_directory(dir_temp)
    # -------------------------------------------------------------
