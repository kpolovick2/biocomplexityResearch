"""MSC_formulation.py - a file containing methods for generating minimum
 set cover problems formulated as a minimum descriptor problem"""
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
    # create an empty output string
    output_string = ""
    # for each row in the dataset
    for (i, row) in enumerate(data):
        # for each item in the row, append it to the string followed by a space
        for column in row:
            output_string += f"{column} "
        # if the row is the last row in the dataset, do not add a newline, otherwise, add a new line character
        if i != len(data) - 1:
            output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"../test_txt_files/MSC_steps/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)


def sort_sets(sets):
    """
    takes a set of sets from the minimum descriptor problem and sorts it by the number of
    items overlapping between that set all other sets divided by the number of items in that set
    :param sets: a list of sets from the minimum descriptor problem
    :return: the list of sets sorted
    """
    # remove duplicates
    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            # if s1 equals s2, and they are not stored in the same index, remove s2
            if s1 == s2 and i != j:
                del sets[j]

    # create an empty list to count overlap
    overlap = [0 for i in range(len(sets))]
    # create a list of the sizes of all sets
    sums = [len(s) for s in sets]

    # create a list that counts the number of overlaps that the set at
    # index i has with all other sets. store that at index i
    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            for e in s1:
                if e in s2 and i != j:
                    overlap[i] += 1

    # divide the number of overlaps by the number of items in the set at index i
    for (i, s) in enumerate(overlap):
        overlap[i] /= sums[i]

    # return the list sets sorted in ascending order of overlap / size
    return [x for _, x in sorted(zip(overlap, sets))]


def reverse_sets(sets):
    """
    takes a set of sets from the minimum descriptor problem and sort them in descending order of size
    :param sets:
    :return:
    """
    # remove duplicates
    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            # if s1 equals s2, and they are not stored in the same index, remove s2
            if s1 == s2 and i != j:
                del sets[j]

    # make a list of the sizes of all descriptors at each index i
    sums = [len(s) for s in sets]

    # return the list of sets sorted in descending order of size
    return list(reversed([x for _, x in sorted(zip(sums, sets))]))


def gen_appendage(sets, num_sets, num_items):
    """
    reduce the minimum set cover problem to the minimum descriptor problem,
    return the portion of the B matrix corresponding to the sets from the minimum
    descriptor problem
    :param sets: a list of the sets from the minimum descriptor problem
    :param num_sets: the number of sets
    :param num_items: the number of items in the universal set
    :return: the portion of the B matrix corresponding to the sets from the minimum
    descriptor problem
    """
    # sort the sets
    sorted_sets = sort_sets(sets)

    # make a B matrix of all zeros
    B = [[0 for i in range(num_sets)] for j in range(num_items)]

    # for each set
    for (i, s) in enumerate(sorted_sets):
        # for each item in the set
        for (j, e) in enumerate(s):
            # set the index of the appendage to 1
            B[e-1][i] = 1

    return B


def gen_sets(num_sets, num_items):
    """
    randomly generate a list of sets from the minimum set cover problem
    :param num_sets: the number of sets to generate
    :param num_items: the number of items in the universal set
    :return: a list of sets fom the minimum set cover problem
    """
    return [sorted(random.sample(range(1, num_items + 1), random.randint(1, num_items))) for i in range(num_sets)]


def get_base(num_sets, num_items):
    """
    generate the base of the minimum set cover problem, which includes
    the first line of the corresponding minimum descriptor problem and the
    diagonal part of the reduction (on the left side of the B matrix) such
    that the minimum descriptor for the "base" is every item in the set
    :param num_sets:
    :param num_items:
    :return:
    """

    # add the first line of the minimum descriptor problem
    data = [[num_items, 1, num_items + num_sets, (num_items + num_sets) * 2, 0]]

    # for each item
    for i in range(num_items):
        # make a row of length num_items + num_sets + 2
        temp = [0 for i in range(num_items + num_sets + 2)]
        # set the first element in the row equal to the number of the item
        temp[0] = i + 1
        # set the second equal to its cluster for compatibility reasons (always 1)
        temp[1] = 1
        # set the tag corresponding to the item equal to 1
        temp[i + 2] = 1
        # add the row to the B matrix
        data.append(temp)

    # return the minimum descriptor problem generated
    return data


def gen_reverse(num_sets, num_items, sets):
    """
    generate msc problems in the form of minimum descriptor problems
    :param num_sets: the number of sets in the msc problem
    :param num_items: the number of items in the universal set
    :param sets: a list of sets in the msc problem
    :return: void
    """
    # generate the part of the minimum descriptor problem that corresponds to the sets of the msc
    appendage = gen_appendage(reverse_sets(sets), num_sets, num_items)
    # generate the base (as previously defined)
    base = get_base(num_sets, num_items)

    # output the base as its own minimum descriptor
    output_file_from_data(base, "MSC", 0)

    # make a deep copy of the base
    full = copy.deepcopy(base)

    # add the appendage to the minimum descriptor problem
    for (i, row) in enumerate(appendage):
        for (j, t) in enumerate(row):
            full[i + 1][j + num_items + 2] = t

    # output the base as its own minimum descriptor problem
    output_file_from_data(full, "MSC", num_sets)

    # generate sequential minimum descriptor problems that correspond
    # to the incremental heuristic solving of the msc problem
    for i in range(num_sets, 0, -1):
        for (j, row) in enumerate(appendage):
            full[j + 1][num_items + i + 1] = 0

        # output each file
        output_file_from_data(full, "MSC", i-1)


def generate_full(num_sets, num_items, sets=None):
    """
    a generation algorithm to generate msc problems in the form of minimum descriptor problems
    :param num_sets: the number of sets to generate
    :param num_items: the number of items to generate
    :param sets: the sets to use if sets are already generated
    :return: the generated sets
    """
    # generate the sets of the minimum descriptor if one is not given
    sets = gen_sets(num_sets, num_items) if sets == None else sets
    # generate the appendage that corresponds to the msc problem generated or given
    appendage = gen_appendage(sets, num_sets, num_items)
    # generate the base for the minimum descriptor problem
    base = get_base(num_sets, num_items)

    # output the base as its own minimum descriptor
    output_file_from_data(base, "MSC", 0)

    # make a deep copy of the base
    full = copy.deepcopy(base)

    # add the appendage to the minimum descriptor problem
    for (i, row) in enumerate(appendage):
        for (j, t) in enumerate(row):
            full[i + 1][j + num_items + 2] = t

    # output the base as its own minimum descriptor problem
    output_file_from_data(full, "MSC", num_sets)

    # generate sequential minimum descriptor problems that correspond
    # to the incremental heuristic solving of the msc problem
    for i in range(num_sets, 0, -1):
        for (j, row) in enumerate(appendage):
            full[j + 1][num_items + i + 1] = 0

        # output the files
        output_file_from_data(full, "MSC", i-1)

    # return the generated sets
    return sets
