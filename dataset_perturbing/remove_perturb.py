"""remove_perturb.py: contains methods for perturbing datasets by deleting tags"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

# this file includes imports of random, math, os, and shutil
from perturb_utilities import *


def remove_single_random(N, cluster, random_percent, percent_removed, cluster_index, delta, current_cluster):
    """
    a helper function that removes a random tag from a single cluster
    :param N: the parameter N of the problem
    :param cluster: a list containing data from each item of a cluster
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param cluster_index: a list that tracks the item numbers of items in the cluster list
    :param delta: a string that will contain the changed tags and their strings
    :param current_cluster: an int that tracks the cluster that is being perturbed
    :return: void
    """
    # choose a tag to remove from the cluster
    tag = random.choice(get_cluster_tags(cluster))
    # decide exactly which items will be perturbed
    items_perturbed = get_items_to_perturb(cluster, random_percent, percent_removed)
    # iterate through the items to be perturbed
    for index in items_perturbed:
        # if the tag is in fact in the item
        if cluster[index][tag] != 0:
            # remove the tag
            cluster[index][tag] = 0
            print(f"removed tag {tag + 1} from item {index} of cluster {current_cluster}, which is item "
                  f"{cluster_index[current_cluster][index]}")
            # note which data item had which tag removed, which will later be stored in the corresponding delta file
            delta += f"{cluster_index[current_cluster][index]}, {tag + 1} \n"
    return delta


def random_single_cluster_internal(filepath, percent_removed, iteration_number, random_percent, dataset_name, cluster):
    """
    helper function to perturb a single cluster with a random amount of tags
    :param filepath: the file path of the dataset
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param iteration_number: the number that should be added to the end of the file's name when generated
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
    :param dataset_name: the name of the dataset
    :param cluster: the cluster to be perturbed
    :return: void
    """
    # parse the dataset
    data = parse_dataset(filepath)

    # use variables to point to parameters in the output file
    n, K, N, alpha, beta = return_parameters(data)

    # convert data into clustered list form
    clusters, cluster_index = convert_clusters(data)

    # generate the deltas based on the removed tags
    delta = remove_single_random(N, clusters[cluster], random_percent, percent_removed, cluster_index, "", cluster)

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

    # generate the final output file of the perturbed data set
    output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


def random_single_cluster(filepath, percent_removed, number_generated, random_percent, cluster):
    """
    perturbs a single cluster, use a random amount of tags
    :param filepath: the file path of the dataset
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param number_generated: the number of perturbed datasets to generate
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
    :param cluster: the cluster to be perturbed
    :return: void
    """

    # ------------------------------------
    # file setup section
    # ------------------------------------

    dataset_name = setup_directories(filepath)

    # ------------------------------------
    # execution section
    # ------------------------------------
    # generate number_generated perturbed datasets
    for i in range(1, number_generated + 1):
        # generation function
        random_single_cluster_internal(filepath, percent_removed, i, random_percent, dataset_name, cluster)


def remove_tag_from_item(filepath, item, tag):
    """
    Removes one tag to one item in a dataset
    :param filepath: the file path of the dataset
    :param item: the item to be perturbed
    :param tag: the tag to be removed
    :return void
    """
    # set up the output directories if they are not already set up
    dataset_name = setup_directories(filepath)
    # parse the input dataset
    data = parse_dataset(filepath)
    # remove the tag from the specified item
    data[item][tag + 1] = 0
    # output the file
    output_file_from_data(data, dataset_name, 0)