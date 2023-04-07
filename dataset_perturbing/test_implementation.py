# test_txt_files/10n_1K_20N_4a_1b.txt

from dataset_perturbing.perturb_utilities import *


def adjust_solution(new_dataset, old_dataset, old_solution):
    new_data = parse_dataset(new_dataset)
    old_data = parse_dataset(old_dataset)

    old_descriptor = {[1] for i in old_solution}
    print(old_descriptor)
    print(old_data[1:])
    for row in old_data[1:]:
        # TODO: implement the rest of this section
        i = row