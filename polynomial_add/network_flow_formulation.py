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
    Runs in O(?) time
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
    :return: a list containing the (indexes + 1) at which 1 is present in the column of the matrix
    """
    vec = []
    for (i, row) in enumerate(mat[1:]):
        # O(n)
        if row[col] == 1:
            vec.append(i+1)
    return vec


def remove_from_set(desc, removed):
    """
    Remove the items from the removed list from the desc list
    :param desc: a descriptor
    :param removed: the tags to remove from said descriptor
    :return:
    """
    new_desc = []
    for (i, t) in enumerate(desc):
        if t not in removed:
            print(f"{i not in removed}")
            new_desc.append(t)
    return new_desc


def recalculate_desc(data, desc, tag_added, items):
    """
    A network flow formulation of the polynomial time tag addition algorithm
    :param data: the dataset being perturbed
    :param desc: the original descriptor
    :param tag_added: the tag to be added to the descriptor
    :param items: the items that tag "covers"
    :return: the updated descriptor
    """
    # create new digraph
    G = nx.DiGraph()
    # make a list to store the items that each tag "covers"
    item_desc = []

    G.add_node("sink")
    G.add_node("source")
    G.add_edge("source", tag_added, capacity=math.inf)
    # add the tag_added node
    G.add_node(tag_added)

    # store n
    n = data[0][0]

    # fill the item_desc list with the items that each tag in the descriptor describes
    for t in desc:
        item_desc.append(get_col(data, t + 1))
        # add the node with name t
        G.add_node(t)

    # create n nodes, each representing an item
    for n in range(1, n+1):
        # add n nodes, each representing an item
        G.add_node(f"i{n}")
        G.add_edge(f"i{n}", "sink")

    # for each list in item_desc, add an edge from the item each tag decribes to the tag
    for (i, l) in enumerate(item_desc):
        for item in l:
            G.add_edge(f"t{desc[i]}", f"i{item}", capacity=1)

    # for each item
    for i in items:
        # add an edge from the tag_added node to the item
        G.add_edge(tag_added, f"i{i}", capacity=1)

    for t in desc:
        G.add_edge("source", t)

    R = None

    # for each tag in the descriptor
    for (i, t) in enumerate(desc):
        # remove the edge between the source and t
        G.remove_edge("source", t)
        # calculate the max flow from the added tag to the descriptor tag
        R = nx.algorithms.flow.preflow_push(G, "source", "sink", residual=R)
        # if the max flow is not equal to the number of items...
        if not R.graph["flow_value"] >= n:
            # add the previous edge back
            G.add_edge("source", t)

    return list(nx.all_neighbors(G, "source"))



file = "1000diagonal.txt"
file_new = "1000diagonal_1.txt"

desc = string_descriptor_to_array(ILP.ILP_one_cluster(f"../test_txt_files/{file}"))[0]
print(update_descriptor_multi_item(f"../test_txt_files/{file}", desc, f"../test_txt_files/{file_new}"))
