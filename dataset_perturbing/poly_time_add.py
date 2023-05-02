"""poly_time_add.py: recalculates the descriptor of a perturbed dataset in polynomial time"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

from perturb_utilities import *
import ILP_linear as ILP


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


def add_single_tag(dataset, desc, tag_added, item):
    """
    Add a single tag to an item in the dataset and return the new descriptor, if updated
    :param dataset: the dataset to be perturbed
    :param desc: the dataset's descriptor
    :param tag_added: the tag that is added
    :param item: the item to add the tag to
    :return: the minimum descriptor of the modified cluster
    """
    # create an empty list to store a list of vectors in the descriptor
    vec_desc = []

    # for each tag in the descriptor
    for tag in desc:
        # add the vector representing the tag of the descriptor
        vec_desc.append(get_col(dataset, tag + 1))

    # find the vector representing the modified column
    added_vec = get_col(dataset, tag_added + 1)
    # add the tag to the modified column
    added_vec[item - 1] = 1

    # a bool that tracks if the tag should be used
    use_tag = False
    # create an empty replaced array
    replaced = []
    # sum the vectors of descriptor tags
    # O(descriptor size * n)
    desc_sum = sum_vectors(vec_desc)
    # add the tag vector of the added tag
    desc_sum = vec_sum(desc_sum, added_vec)

    # O(descriptor size * n)
    for (i, v) in enumerate(vec_desc):
        # could speed up by removing copy in the sum and diff functions, making this a mutation
        # O(2n) = O(n)
        if min(vec_diff(desc_sum, v)) >= 1:
            # add the tag to the list of replaced tags
            replaced.append(i)
            # update use_tag
            use_tag = True

    # copy the descriptor
    # O(descriptor size)
    new_desc = desc.copy()
    # for each index in replaced
    # O(descriptor size)
    for idx in replaced:
        # replace the tag with -1 (intentionally out of bounds)
        new_desc[idx] = -1

    # if the tag should be appended, append it
    # O(1)
    new_desc.append(tag_added) if use_tag else None

    # remove all -1 tags from the descriptor
    # O(descriptor size)
    new_desc = [i for i in new_desc if i != -1]

    # if the descriptor is improved, return it
    # O(1)
    if len(new_desc) < len(desc):
        # O(descriptor size log (descriptor size))
        return sorted(new_desc)

    # if not, return the original descriptor
    return desc


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

    # a bool that tracks if the tag should be used
    use_tag = False
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
        # could speed up (physically, not asymptotically)
        # by removing copy in the sum and diff functions, making this a mutation
        if min(vec_diff(desc_sum, v)) >= 1:
            # add the tag to the list of replaced tags
            replaced.append(i)
            # update use_tag
            use_tag = True

    # copy the descriptor
    new_desc = desc.copy()
    # for each index in replaced
    for idx in replaced:
        # replace the tag with -1 (intentionally out of bounds)
        new_desc[idx] = -1

    # if the tag should be appended, append it
    # O(1)
    new_desc.append(tag_added) if use_tag else None

    # remove all -1 tags from the descriptor
    # O(descriptor size)
    new_desc = [i for i in new_desc if i != -1]

    # if the descriptor is improved, return it
    # O(descriptor size * log(descriptor size))
    #       amortized O(n)
    # could be reduced to O(n) by partitioning around the singular tag
    # not worth the time because it already runs in O(n) time because it's one tag
    if len(new_desc) < len(desc):
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
    # parse the new dataset
    new_dataset = parse_dataset(new_data)
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


data1 = parse_dataset(f"../test_txt_files/add_perturb_test_1K.txt")
desc1 = string_descriptor_to_array(ILP.ILP_linear(f"../test_txt_files/add_perturb_test_1K.txt"))[0]
tag_added1 = 5
item1 = [2, 4]

print(f"New Descriptor: {add_multi_item(data1, desc1, tag_added1, item1)}")
print(update_descriptor_multi_item(f"../test_txt_files/add_perturb_test_1K.txt", desc1,
                                   f"../test_txt_files/add_perturb_test_1K_2.txt"))
