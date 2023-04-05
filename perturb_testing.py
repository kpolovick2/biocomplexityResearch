# William Bradford
# wcb8ze
# central perturb testing file

import add_perturb, descriptor_comparison

add_perturb.random_all_clusters("test_txt_files/9x28.txt", 50, 3, True)
descriptor_comparison.find_descriptors("9x28")