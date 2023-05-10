"""poly_add_mem.py: recalculates the descriptor of a perturbed dataset in polynomial time using
more memory efficient means.
This file is an alternate version of poly_add.py, which uses a more memory efficient version of the same algorithm."""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

from dataset_perturbing.perturb_utilities import *
import one_cluster_ilp as ILP


def get_col(mat, col):
    """
    a helper function that returns a column from a list of lists
    :param mat: a matrix (list of lists)
    :param col: a column
    :return: a list containing the indexes at which 1 is present in the column of the matrix
    """
    vec = []
    for (i, row) in enumerate(mat[1:]):
        # O(n)
        if row[col] == 1:
            vec.append(i)
    return vec


def vec_sum(v1, idxs):
    """
    Takes a vector and the indexes at which one should be addded, returns the result
    :param v1: a vector
    :param idxs: the indexes at which one should be added
    :return: the sum of the two "vectors"
    """
    for i in idxs:
        v1[i] += 1
    return v1


def vec_diff(v1, idxs):
    """
    Takes a vector and the indexes at which one should be subtracted, returns the result
    :param v1: a vector
    :param idxs: the indexes at which one should be subtracted
    :return: the difference of the two "vectors"
    """
    for i in idxs:
        v1[i] -= 1
    return v1


def add_vecs(v1, v2):
    """
    Add two vectors
    :param v1: vector 1
    :param v2: vector 2
    :return: v1 + v2
    """
    for (i, val) in enumerate(v2):
        v1[i] += val
    return v1


def sum_desc(V, n):
    """
    Sums the vectors in list V
    :param V: a list of vectors, stored in the form of indexes at which a 1 is present
    :param n: the number of items in the dataset
    :return: the sum of each of the descriptor vectors
    """
    sum = [0 for i in range(n)]
    for v in V:
        for idx in v:
            sum[idx] += 1
    return sum


def remove_from_set(desc, removed):
    """
    Takes a descriptor in list form, removes the list removed from it
    :param desc: a descriptor
    :param removed: a list of tags to remove
    :return: a copy of the descriptor without any tags present in removed
    """
    new_desc = []
    for (i, t) in enumerate(desc):
        if t not in removed:
            new_desc.append(t)
    return new_desc


def add_multi_item(dataset, desc, tag_added, items):
    """
    Add a single tag to multiple items in a dataset and return the new descriptor, if updated
    :param dataset: the dataset to be perturbed
    :param desc: the dataset's descriptor
    :param tag_added: the tag that is added
    :param items: the list of items that the tag should be added to
    :return: the minimum descriptor of the modified cluster
    """
    # create an empty list to store a list of vectors in the descriptor
    vec_desc = []

    # for each tag in the descriptor
    # O(descriptor size)
    for tag in desc:
        # add the vector representing the tag of the descriptor
        vec_desc.append(get_col(dataset, tag + 1))

    # find the vector representing the modified column
    added_vec = get_col(dataset, tag_added + 1)
    # add the tag to the item slot in the vector
    # O(n)
    for item in items:
        # add the tag to the modified column
        added_vec.append(item)

    # create an empty replaced array
    replaced = []
    # sum the vectors of descriptor tags
    # O(descriptor size * n)
    desc_sum = sum_desc(vec_desc, dataset[0][0])
    # add the tag vector of the added tag
    # O(n)
    desc_sum = add_vecs(desc_sum, added_vec)

    # O(descriptor size * n)
    for (i, v) in enumerate(vec_desc):
        # subtract the corresponding vector
        vec_diff(desc_sum, v)
        # if the minimum of the vector is greater than or equal to 1
        if min(desc_sum) >= 1:
            # add the tag to the list of replaced tags
            replaced.append(i)
        else:
            # add the vector back to the descriptor sum
            vec_sum(desc_sum, v)

    # if more than one tag is removed
    if len(replaced) > 1:
        # generate the new descriptor without tag_added
        new_desc = remove_from_set(desc, replaced)
        # add tag_added
        new_desc.append(tag_added)
        # return the sorted list
        return sorted(new_desc)

    # if not, return the original descriptor
    return desc


def update_descriptor_multi_item(data, desc, new_data):
    """
    Given two files representing a dataset and a perturbed version of
    that dataset, return the modified descriptor
    This method can only handle single tag perturbations of multiple item, where all tags are the same
    Runs in O(n*N + descriptor size * n) time
    :param data: the initial dataset
    :param desc: the initial descriptor
    :param new_data: the new dataset after perturbation
    :return:
    """
    # parse the initial dataset
    dataset = parse_dataset(data)
    dataset = dataset[:-1] if len(dataset[-1]) == 0 else dataset
    # parse the new dataset
    new_dataset = parse_dataset(new_data)
    new_dataset = new_dataset[:-1] if len(new_dataset[-1]) == 0 else new_dataset
    # placeholder tag added
    tag_added = -1
    # empty list of items
    items = []
    # for each item in the dataset
    # O(n * N)
    for (i, item) in enumerate(dataset):
        # for each tag value in the item
        for (j, t) in enumerate(item):
            # if the two datasets do not match
            if t != new_dataset[i][j]:
                # set tag_added to the tag
                tag_added = j - 1
                # add i to the list of items
                items.append(i)

    return add_multi_item(dataset, desc, tag_added, items)


# dataset = parse_dataset(f"../test_txt_files/add_perturb_test_1K.txt")
# desc = [1, 5, 7, 8]
# tags = [1, 2]
# items = [[1], [1, 2, 3, 4]]
#
# print(add_tags(dataset, desc, tags, items))
#
# file = "10diagonal.txt"
# file_new = "10diagonal_1.txt"
#
# desc = string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/{file}"))[0]
# print(update_descriptor_multi_item(f"../test_txt_files/{file}", desc, f"../test_txt_files/{file_new}"))