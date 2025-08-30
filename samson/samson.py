# Aug-25-2025
# samson.py

"""
How to use: python samson.py
"""

from pathlib import Path
from distances import distances
from clustering import clustering
from get_tabular_results import get_tabular_results
from utils.src.dir_support import files_number_in_directory


def main():
    dir_basket = Path.cwd() / 'BASKET'
    n_objects = files_number_in_directory(dir_basket)

    print(f'\nS A M S O N')
    print(f'There are {n_objects} objects in the BASKET folder.')
    input_string \
        = input('Please enter the desired number of clusters: ')
    number_of_clusters = int(input_string)

    D = distances(dir_basket)

    clustering(D, number_of_clusters)

    get_tabular_results()   # result in the directory "OUTPUT"


if __name__ == "__main__":
    main()
