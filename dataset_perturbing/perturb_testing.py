"""perturb_testing.py: the main file for executing perturbations of datasets"""
__author__ = "William Bradford, Keara Polovick"
__email__ = "wcb8ze@virginia.edu, uzy2ws@virginia.edu"

import add_perturb
import remove_perturb
import descriptor_comparison

dataset = "1000n_6K_40N_4a_1b"

# on the dataset "9x28," the test statistic of the test for absence of correlation is -1.2525
#               this means that the p-value is 0.23, meaning we do not have enough evidence to reject
#               the hypothesis that there is not any correlation between the number of items with
#               1 tag added and the size decrease in the descriptor

# add_perturb.add_tag_to_item(f"../test_txt_files/{dataset}.txt", 1, 1)
add_perturb.multitag_random_single_cluster(f"../test_txt_files/{dataset}.txt", 50, 1, True, 1, 6, 1, 40)
descriptor_comparison.find_descriptors_added(dataset)
