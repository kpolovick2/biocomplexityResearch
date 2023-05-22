import poly_add as pa
import dataset_perturbing.perturb_utilities as ptu
import one_cluster_ilp as ILP
import solution_checker as checker
import random
import MSC_formulation


def output_file_from_data(data, dataset_name, iteration_number):
    """
    uses a dataset in list format to generate an output file
    :param data: a dataset in list format
    :param dataset_name: the name of the dataset
    :param iteration_number: the number that should be appended to the end of the filename
    :return: void
    """
    output_string = ""
    for (i, row) in enumerate(data):
        for column in row:
            output_string += f"{column} "
        if i != len(data) - 1:
            output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"../test_txt_files/MSC_steps/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)


def generate_sets(num_sets, num_items=4):
    sets = [[random.randint(0, 1) for i in range(num_sets)] for i in range(num_items)]
    return sets


def gen_MSC(sets):
    MSC_base = ptu.parse_dataset(f"../test_txt_files/MSC_steps/MSC_0.txt")

    output_file_from_data(MSC_base, "MSC", 0)

    MSC_full_problem = MSC_base.copy()
    for (i, row) in enumerate(sets):
        for (j, t) in enumerate(row):
            MSC_full_problem[i+1][j+6] = t

    output_file_from_data(MSC_full_problem, "MSC", "full_problem")

    for (i, row) in enumerate(sets):
        MSC_full_problem[i + 1][len(row) + 5] = 0

    output_file_from_data(MSC_full_problem, "MSC", 3)

    for (i, row) in enumerate(sets):
        MSC_full_problem[i + 1][len(row) + 4] = 0

    output_file_from_data(MSC_full_problem, "MSC", 2)

    for (i, row) in enumerate(sets):
        MSC_full_problem[i + 1][len(row) + 3] = 0

    output_file_from_data(MSC_full_problem, "MSC", 1)


def test_msc(num_sets, num_items):
    print(MSC_formulation.generate_full(num_sets, num_items))

    initial = ptu.string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/MSC_steps/MSC_0.txt"))[0]
    final = ptu.string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/MSC_steps/MSC_{num_sets}.txt"))[0]

    temp_desc = initial.copy()

    for i in range(num_sets):
        temp_desc = pa.update_descriptor_multi_item(f"../test_txt_files/MSC_steps/MSC_{i}.txt", temp_desc,
                                             f"../test_txt_files/MSC_steps/MSC_{i+1}.txt")

    print(f"The ILP solution: {final}")
    print(f"The polynomial time solution: {temp_desc}")

    if checker.check_descriptor(temp_desc, f"../test_txt_files/MSC_steps/MSC_{num_sets}.txt") \
            and len(temp_desc) == len(final):
        print("Solution working")
    else:
        print("Solution NOT working")
        raise Exception(f"Solution is not a minimum descriptor: \n Polynomial solution: {temp_desc} / ILP solution: {final}")


while True:
    test_msc(5, 9)
