"""test_implementation.py: an unused testing file for designing an
algorithm to adjust descriptors after perturbing a dataset"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

from dataset_perturbing.perturb_utilities import *

def adjust_solution(new_dataset, old_dataset, old_solution):
    new_data = parse_dataset(new_dataset)
    old_data = parse_dataset(old_dataset)

    old_descriptor = {i: [] for i in old_solution}
    print(old_descriptor)
    for row in old_data[1:len(old_data) - 1]:
        for i in list(old_descriptor.keys()):
            old_descriptor[i].append(row[i])

    print(old_descriptor)

adjust_solution("perturb_data/300n_6K_40N_4a_1b.txt/300n_6K_40N_4a_1b.txt.txt",
                "perturb_data/300n_6K_40N_4a_1b.txt/300n_6K_40N_4a_1b.txt.txt", [5, 19])
