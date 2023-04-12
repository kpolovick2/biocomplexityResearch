"""perturb_testing.py: the main file for executing perturbations of datasets"""
__author__ = "William Bradford, Keara Polovick"
__email__ = "wcb8ze@virginia.edu"

import add_perturb
import remove_perturb
import descriptor_comparison

dataset = "9x28"

# add_perturb.add_tag_to_item(f"../test_txt_files/{dataset}.txt", 1, 1)
remove_perturb.random_all_clusters(f"../test_txt_files/{dataset}.txt", 50, 120, True)
# descriptor_comparison.find_descriptors_added(dataset)
