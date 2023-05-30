import polynomial_add.poly_add as pa
import dataset_perturbing.perturb_utilities as pu


def find_uncovered(desc_sum):
    """
    find the indices of uncovered parts of the given descriptor
    :param desc_sum: the sum of all vectors of the descriptor
    :return: the uncovered elements by index
    """
    uncovered = []
    for (i, num) in enumerate(desc_sum):
        if num <= 0:
            uncovered.append(i)
    return uncovered


def unique_test(data, desc):
    """
    a method that takes a dataset and a minimum descriptor and returns True if that descriptor
    is the only minimum descriptor for that dataset
    note: this function does not work on "zipper cases"
    not correct unless p = np because reduces to k-msc:
        same formulation as previous reduction
        add k arbitrary sets that guaranteed cover the universal set on the right side of the minimum descriptor problem
        if there is another descriptor of size k, then the original problem had a descriptor of size k and thus had
            a minimum set cover of size k
    thus the uniqueness test is an NP-hard problem
    :param data: the dataset for the ilp
    :param desc: the minimum descriptor for the ilp
    :return: a bool specifying if the minimum descriptor is unique
    """
    # parse the initial dataset
    dataset = pu.parse_dataset(data)
    dataset = dataset[:-1] if len(dataset[-1]) == 0 else dataset

    vec_desc = []
    # for each tag in the descriptor
    # O(descriptor size)
    for tag in desc:
        # add the vector representing the tag of the descriptor
        vec_desc.append(pa.get_col(dataset, tag + 1))

    desc_sum = pa.sum_vectors(vec_desc)

    exclusive_coverage = []

    for (i, v) in enumerate(vec_desc):
        pa.mut_vec_diff(desc_sum, v)
        exclusive_coverage.append(find_uncovered(desc_sum))
        pa.mut_vec_sum(desc_sum, v)

    N = dataset[0][2]
    for (i, t) in enumerate(desc):
        for j in range(1, N+1):
            if j not in desc:
                ec = []
                for item in exclusive_coverage[i]:
                    if dataset[item + 1][j + 1] == 1:
                        ec.append(item)
                if ec == exclusive_coverage[i]:
                    return False

    return True


print(unique_test("../test_txt_files/10diagonal.txt", [1, 2, 4, 10]))
