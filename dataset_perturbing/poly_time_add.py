from perturb_utilities import *
import ILP_linear as ILP


def get_col(mat, col):
    vec = []
    for row in mat[1:]:
        # O(n)
        vec.append(row[col])
    return vec

def sum_vectors(vector_list):
    sum = [0 for i in range(len(vector_list[0]))]
    for v in vector_list:
        for i in range(len(v)):
            sum[i] += v[i]
    return sum


def add_single_tag(dataset, desc, tag_added, item):
    """
    Add a single tag to a dataset and return the new descriptor, if updated
    :param dataset: the dataset to be perturbed
    :param desc: the dataset's descriptor
    :param tag_added: the tag that is added
    :return:
    """
    vec_desc = []

    # for each tag in the descriptor
    for tag in desc:
        # add the vector representing the tag of the descriptor
        vec_desc.append(get_col(dataset, tag + 1))

    # find the vector representing the modified column
    added_vec = get_col(dataset, tag_added + 1)
    # add the tag to the modified column
    added_vec[item-1] = 1

    use_tag = False
    replaced = []
    for (i, v) in enumerate(vec_desc):
        vec_desc_copy = vec_desc.copy()
        vec_desc_copy[i] = added_vec
        # new proposition:
        # sum them, store that, then add added_vec
        # if added_vec has min >= 2, then we know the tag should be added
        # then iterate by subtracting the vector that is no longer being considered
        # and adding added_vec
        if min(sum_vectors(vec_desc_copy)) != 0:
            replaced.append(i)
            use_tag = True

    new_desc = desc.copy()
    for idx in replaced:
        new_desc[idx] = 0

    if use_tag:
        new_desc.append(tag_added)

    while min(new_desc) == 0:
        new_desc.remove(0)

    if len(new_desc) < len(desc):
        return new_desc

    return desc


data = parse_dataset(f"../test_txt_files/add_perturb_test_1K.txt")
desc = string_descriptor_to_array(ILP.ILP_linear(f"../test_txt_files/add_perturb_test_1K.txt"))[0]
tag_added = 8
item = 2

print(f"New Descriptor: {add_single_tag(data, desc, tag_added, item)}")
