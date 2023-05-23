import poly_add as pa
import dataset_perturbing.perturb_utilities as ptu
import one_cluster_ilp as ILP
import solution_checker as checker
import MSC_formulation


def test_msc(num_sets, num_items):
    """
    a test housing to confirm that the
    :param num_sets: 
    :param num_items: 
    :return: 
    """
    s = MSC_formulation.generate_full(num_sets, num_items)

    initial = ptu.string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/MSC_steps/MSC_0.txt"))[0]
    final = ptu.string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/MSC_steps/MSC_{num_sets}.txt"))[0]

    temp_desc = initial.copy()

    for i in range(num_sets):
        temp_desc = pa.update_descriptor_multi_item(f"../test_txt_files/MSC_steps/MSC_{i}.txt", temp_desc,
                                             f"../test_txt_files/MSC_steps/MSC_{i+1}.txt")

    desc_1 = temp_desc.copy()

    temp_desc = initial.copy()

    MSC_formulation.generate_reverse(num_sets, num_items, s)

    for i in range(num_sets):
        temp_desc = pa.update_descriptor_multi_item(f"../test_txt_files/MSC_steps/MSC_{i}.txt", temp_desc,
                                                    f"../test_txt_files/MSC_steps/MSC_{i + 1}.txt")

    temp_desc = temp_desc if len(temp_desc) < len(desc_1) else desc_1

    print(f"The ILP solution: {final}")
    print(f"The polynomial time solution: {temp_desc}")

    # the cases are:
    # check that the descriptor describes the cluster
    # check that the length of the two descriptors are the same
    if checker.check_descriptor(temp_desc, f"../test_txt_files/MSC_steps/MSC_{num_sets}.txt") \
            and len(temp_desc) == len(final):
        print("Solution working")
    # elif min(final) <= num_sets:
    #     print("Solution does not have a minimum descriptor")
    else:
        print("Solution NOT working")
        if len(temp_desc) - 1 > len(final):
            raise Exception(f"Solution is not a minimum descriptor: \n Polynomial solution: {temp_desc} "
                            f"/ ILP solution: {final}"
                            f"sets = {s}")


while True:
    test_msc(12, 12)
