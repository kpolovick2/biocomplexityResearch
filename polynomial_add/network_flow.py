from dataset_perturbing.perturb_utilities import *
import networkx as nx
import one_cluster_ilp as ILP

# add node for each tag in descriptor, which connects with edges to a node for each item
# add


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

    return recalculate_desc(dataset, desc, tag_added, items)


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
            vec.append(i+1)
    return vec


def remove_from_set(desc, removed):
    new_desc = []
    for (i, t) in enumerate(desc):
        if t not in removed:
            print(f"{i not in removed}")
            new_desc.append(t)
    return new_desc


def recalculate_desc(data, desc, tag_added, items):
    G = nx.DiGraph()
    item_desc = []

    n = data[0][0]

    for t in desc:
        item_desc.append(get_col(data, t + 1))

    for n in range(1, n+1):
        # add n nodes, each representing an item
        G.add_node(f"i{n}")

    G.add_node(f"tag_added")

    for t in desc:
        G.add_node(f"t{t}")

    for (i, l) in enumerate(item_desc):
        for item in l:
            G.add_edge(f"i{item}", f"t{desc[i]}", capacity=1)

    for i in items:
        G.add_edge("tag_added", f"i{i}", capacity=1)

    G.add_node("sink")

    replaced = []

    for (i, t) in enumerate(desc):
        f = nx.maximum_flow_value(G, "tag_added", f"t{t}")
        if f == len(item_desc[i]):
            replaced.append(t)

    if len(replaced) > 1:
        new_desc = remove_from_set(desc, replaced)
        new_desc.append(tag_added)
        return sorted(new_desc)

    return desc



# file = "10diagonal.txt"
# file_new = "10diagonal_1.txt"
#
# desc = string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/{file}"))[0]
# print(update_descriptor_multi_item(f"../test_txt_files/{file}", desc, f"../test_txt_files/{file_new}"))
