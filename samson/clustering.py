# Aug-25-2025
# clustering.py

import shutil
import numpy as np
from pathlib import Path

from utils.src.dir_support import reset_directory, read_directory_data
from utils.src.file_support import get_filenames_from_filepaths


# 1 of 6
# -------------------------------------------------------------
# clustering_method = 1   # минимальное локальное расстояние
# clustering_method = 2   # максимальное локальное расстояние
# clustering_method = 3   # медиана
# clustering_method = 4   # среднее группы
# clustering_method = 5   # центроидный
clustering_method = 6   # метод Ворда
# -------------------------------------------------------------

def clustering(D, number_of_clusters):
    global clustering_method

    dir_basket_24bpp = Path.cwd() / 'BASKET_24bpp'
    list_basket_paths = read_directory_data(dir_basket_24bpp)
    list_basket_paths.sort()
    n_objects = len(list_basket_paths)
    n_objects_1 = n_objects - 1             # number of mergers

    # ---------------------------------------------------------
    reset_directory('CLUSTERS')

    # This line of Python code creates a 2-dimensional list
    # (a list of lists) named clusters.
    clusters = [['' for i in range(n_objects)] for j in range(n_objects)]

    list_names = get_filenames_from_filepaths(list_basket_paths)

    m = 0
    for n in range(n_objects):
        filename = list_names[n]
        clusters[n][m] = filename
        m += 1
    # ---------------------------------------------------------

    # N[] - начальное количество объектов в каждом кластере
    N = np.ones(n_objects, dtype=np.int32)

    # ---------------------------------------------------------
    for k in range(n_objects_1):

        # Определение минимального значения
        # в матрице D выше диагонали
        # -----------------------------------------------------
        minD = np.finfo(float).max      # max float

        i = -1
        j = -1
        for row in range(n_objects_1):
            if N[row] == 0:
                continue

            for col in range(row+1, n_objects):
                if N[col] == 0:
                    continue

                if D[row, col] < minD:
                    minD = D[row, col]
                    j = row
                    i = col
        # -----------------------------------------------------

        # Пересчет после слияния.
        # -----------------------------------------------------
        temp = 0.0

        for h in range(n_objects):

            if N[h] == 0:
                continue

            match clustering_method:

                case 1: # минимальное локальное расстояние
                        temp = (D[h, i] + D[h, j] - abs(D[h, i] - D[h, j])) * 0.5

                case 2: # максимальное локальное расстояние
                        temp = (D[h, i] + D[h, j] + abs(D[h, i] - D[h, j])) * 0.5

                case 3: # медиана
                        temp = (D[h, i] + D[h, j]) * 0.5 + minD * 0.25

                case 4: # среднее группы
                        coeff_1 = N[i] / (N[i] + N[j])
                        coeff_2 = N[j] / (N[i] + N[j])
                        temp = coeff_1 * D[h, i] + coeff_2 * D[h, j]

                case 5: # центроидный
                        coeff_1 = N[i] / (N[i] + N[j])
                        coeff_2 = N[j] / (N[i] + N[j])
                        coeff_3 = (N[i] * N[j]) / ((N[i] + N[j]) * (N[i] + N[j]))
                        temp = coeff_1 * D[h, i] + coeff_2 * D[h, j] - coeff_3 * minD

                case 6: # метод Ворда
                        coeff = 1 / (N[h] + N[i] + N[j])
                        temp = coeff * ((N[h] + N[i]) * D[h, i] + (N[h] + N[j]) * D[h, j] -
                                    N[h] * minD)

            D[i, h] = temp
            D[h, i] = temp

        for h in range(n_objects):
            D[j, h] = 0.0
            D[h, j] = 0.0
        # -----------------------------------------------------

        # При слиянии в кластер с большим индексом добавляются объекты
        # из кластера с меньшим индексом. При этом, кластер с меньшим
        # индексом удаляется из дальнейшего рассмотрения: N[j] = 0
        # -----------------------------------------------------
        N[i] += N[j]        # N[] - количество объектов в кластере.
        N[j] = 0

        for n in range(n_objects):
            if clusters[j][n] != '':
                clusters[i][n] = clusters[j][n]
        # -----------------------------------------------------

        if (n_objects_1 - k) == number_of_clusters:
            break

    # Saving the contents of each cluster
    for n in range(n_objects):
        if N[n] > 0:
            for item in clusters[n]:
                if item != '':
                    # print(f'\t {item}')

                    dir_cluster = Path.cwd() / 'CLUSTERS' / str(n)
                    if not dir_cluster.exists():
                        dir_cluster.mkdir()

                    path_src = dir_basket_24bpp / item
                    path_dst = dir_cluster / item
                    shutil.copy(path_src, path_dst)
