import timeit
import one_cluster_ilp as ILP
import dataset_perturbing.perturb_utilities as ptu

test_count = 12

orig_file = "1000diagonal.txt"
file = "1000diagonal_1.txt"

desc = ptu.string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/{orig_file}"))[0]

ilp_time = timeit.timeit(f"a.ILP_linear('../test_txt_files/{file}')",  setup="import ILP_linear as a",
                         number=test_count)
revised_time = timeit.timeit(f"print(p.update_descriptor_multi_item('../test_txt_files/{orig_file}',"
                             f" {desc}, '../test_txt_files/{file}'))", setup="import poly_add_mem as p", number=test_count)

print(f"The ILP solved this problem in {ilp_time/test_count} seconds per execution.")
print(f"The polynomial time add algorithm solved this problem in {revised_time/test_count} seconds per execution.")
print(f"The polynomial algorithm was {ilp_time/revised_time} times faster.")
