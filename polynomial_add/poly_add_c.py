from dataset_perturbing.perturb_utilities import *
import one_cluster_ilp as ILP
from numba import jit
import numpy as np


def get_col(mat, col):
    """
    a helper function that returns a column from a list of lists
    :param mat: a matrix (list of lists)
    :param col: a column
    :return: a list containing the values of the specified column of the matrix
    """
    vec = []
    for row in mat[1:]:
        # O(n)
        vec.append(row[col])
    return vec


def sum_vectors(vector_list):
    """
    sums a list of lists at each i value
    :param vector_list: a list of lists
    :return: a list that contains the sum of each list v[i] at each i value
    """
    sum = [0 for i in range(len(vector_list[0]))]
    for v in vector_list:
        for i in range(len(v)):
            sum[i] += v[i]
    return sum


def vec_sum(v1, v2):
    """
    sums two lists at each i value
    :param v1: list 1
    :param v2: list 2
    :return: a list containing the sum of v1[i] + v2[i] at list[i]
    """
    sum = v1.copy()
    for (i, v) in enumerate(v2):
        sum[i] += v
    return sum


def vec_diff(v1, v2):
    """
    takes the difference of two lists at each i value
    :param v1: list 1
    :param v2: list 2
    :return: a list containing the sum of v1[i] - v2[i] at list[i]
    """
    sum = v1.copy()
    for (i, v) in enumerate(v2):
        sum[i] -= v
    return sum


def mut_vec_sum(v1, v2):
    """
    returns the sum of two vectors stored in the first vector
    :param v1: the first vector
    :param v2: the second vector
    :return: void
    """
    for (i, v) in enumerate(v2):
        v1[i] += v


def mut_vec_diff(v1, v2):
    """
    returns the difference between two vectors stored in the first vector
    :param v1: the first vector
    :param v2: the second vector
    :return: void
    """
    min = math.inf
    for (i, v) in enumerate(v2):
        v1[i] -= v
        min = v1[i] if v1[i] < min else min
    return min


@jit(nopython=True)
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
        added_vec[item - 1] = 1

    # create an empty replaced array
    replaced = []
    # sum the vectors of descriptor tags
    # O(descriptor size * n)
    desc_sum = sum_vectors(vec_desc)
    # add the tag vector of the added tag
    # O(n)
    desc_sum = vec_sum(desc_sum, added_vec)

    # O(descriptor size * n)
    for (i, v) in enumerate(vec_desc):
        min = mut_vec_diff(desc_sum, v)
        if min >= 1:
            # add the tag to the list of replaced tags
            replaced.append(i)
        else:
            mut_vec_sum(desc_sum, v)

    if len(replaced) > 1:
        new_desc = remove_from_set(desc, replaced)
        new_desc.append(tag_added)
        return new_desc

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


def remove_from_set(desc, removed):
    new_desc = []
    for (i, t) in enumerate(desc):
        if i not in removed:
            new_desc.append(t)
    return new_desc
