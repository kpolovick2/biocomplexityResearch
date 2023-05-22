import copy
import random


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


def sort_sets(sets):
    overlap = [0 for i in range(len(sets))]

    # remove duplicates
    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            if s1 == s2 and i != j:
                del sets[j]

    # count the overlap
    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            for e in s1:
                if e in s2 and i != j:
                    overlap[i] += 1

    # return the list sets sorted in ascending order of overlap
    return [x for _, x in sorted(zip(overlap, sets))]


def gen_appendage(sets, num_sets, num_items):
    sorted_sets = sort_sets(sets)
    B = [[0 for i in range(num_items)] for j in range(num_sets)]

    for (i, s) in enumerate(sorted_sets):
        for (j, e) in enumerate(s):
            B[e-1][i] = 1

    return B


def gen_sets(num_sets, num_items):
    return [sorted(random.sample(range(1, num_items + 1), random.randint(1, num_items))) for i in range(num_sets)]


def get_base(num_sets, num_items):
    data = [[num_items, 1, num_items + num_sets, (num_items + num_sets) * 2, 0]]

    for i in range(num_items):
        temp = [0 for i in range(num_items + num_sets + 2)]
        temp[0] = i + 1
        temp[1] = 1
        temp[i + 2] = 1
        data.append(temp)

    return data

def generate_full(num_sets, num_items):
    appendage = gen_appendage(gen_sets(num_sets, num_items), num_sets, num_items)
    base = get_base(num_sets, num_items)

    output_file_from_data(base, "MSC", 0)

    full = copy.deepcopy(base)

    for (i, row) in enumerate(appendage):
        for (j, t) in enumerate(row):
            full[i + 1][j + num_items + 2] = t

    output_file_from_data(full, "MSC", "full_problem")

    for i in range(num_sets, 0, -1):
        for (j, row) in enumerate(appendage):
            full[j + 1][num_items + i + 1] = 0

        output_file_from_data(full, "MSC", i-1)


S = [[1, 3], [1, 2], [3, 4], [1, 3]]

print(gen_appendage(gen_sets(4, 4), 4, 4))
get_base(4, 4)
generate_full(4, 4)
