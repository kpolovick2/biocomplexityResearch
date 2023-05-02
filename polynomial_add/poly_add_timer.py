import timeit


test_count = 12000

ilp_time = timeit.timeit(f"a.ILP_linear('../test_txt_files/add_perturb_test_1K_2.txt')",  setup="import ILP_linear as a",
              number=test_count)
revised_time = timeit.timeit("p.update_descriptor_multi_item('../test_txt_files/add_perturb_test_1K.txt',"
                             " [1, 5, 7, 8], '../test_txt_files/add_perturb_test_1K_2.txt')", setup="import poly_add as p", number=test_count)

print(ilp_time)
print(revised_time)