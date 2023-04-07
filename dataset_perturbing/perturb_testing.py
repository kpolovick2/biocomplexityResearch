# William Bradford
# wcb8ze
# central perturb testing file

import add_perturb, descriptor_comparison

dataset = "10n_1K_20N_4a_1b"

add_perturb.random_single_cluster(f"../test_txt_files/{dataset}.txt", 50, 3, True, 1)
descriptor_comparison.find_descriptors(dataset)
