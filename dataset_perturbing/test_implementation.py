# William Bradford
# wcb8ze
# an unused testing file for designing an algorithm to adjust descriptors after perturbing a dataset
# test_txt_files/10n_1K_20N_4a_1b.txt

from dataset_perturbing.perturb_utilities import *


def adjust_solution(new_dataset, old_dataset, old_solution):
    new_data = parse_dataset(new_dataset)
    old_data = parse_dataset(old_dataset)

    old_descriptor = {i : [] for i in old_solution}
    print(old_descriptor)
    for row in old_data[1:len(old_data)-1]:
        for i in list(old_descriptor.keys()):
            old_descriptor[i].append(row[i])

    print(old_descriptor)


adjust_solution("perturb_data/10n_1K_20N_4a_1b/10n_1K_20N_4a_1b.txt", "perturb_data/10n_1K_20N_4a_1b/10n_1K_20N_4a_1b_1.txt", [5, 19])