# William Bradford
# wcb8ze
# central perturb testing file

import add_perturb, descriptor_comparison

dataset = "9x28"

add_perturb.random_all_clusters(f"test_txt_files/{dataset}.txt", 50, 3, True)
descriptor_comparison.find_descriptors(dataset)