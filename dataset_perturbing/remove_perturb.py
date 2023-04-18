"""remove_perturb.py: contains methods for perturbing datasets by deleting tags"""
__author__ = "William Bradford, Keara Polovick"
__email__ = "wcb8ze@virginia.edu, uzy2ws@virginia.edu"

# this file includes imports of random, math, os, and shutil
from perturb_utilities import *


def has_only_one_tag(item):
    """
    a helper function to determine if an item has only one tag
    :param item: an item in list form
    :return: bool representing whether the item has only one tag
    """
    # initialize a tag count
    tag_count = 0
    # for each tag in the item
    for tag in item:
        # if the item has the tag
        if tag == 1:
            # increment tag count
            tag_count += 1
        # if the tag count is greater than one
        if tag_count > 1:
            # early exit
            return tag_count == 1
    # return true if tag_count == 1
    return tag_count == 1

def get_items_to_remove(cluster, random_percent, percent_added):
    """
    a helper function that returns a list of items to perturb
    :param cluster: a cluster in list form
    :param random_percent: a boolean determining whether the percent of items perturbed is random
    :param percent_added: a percent (0-100) of the items in the cluster that should be perturbed
    :return: a list of items to be perturbed
    """
    cluster_size = len(cluster)
    items_with_one_tag = [i for i, item in enumerate(cluster) if has_only_one_tag(item)]
    print(items_with_one_tag)
    # perturb at most percent_added percent of the cluster
    if cluster_size == 0:
        # if the cluster is empty (which should only happen in the 0 cluster), do not perturb any tags
        num_items_perturbed = 0
    elif random_percent:
        # if random_percent is true, then pick a random number of tags to perturb
        num_items_perturbed = random.choice(range(1, cluster_size + 1))
    else:
        # if random_percent is false, find the percentage of the items in the cluster to be perturbed
        num_items_perturbed = math.floor(percent_added / 100 * cluster_size)
    # decide exactly which items will be perturbed
    items_perturbed = random.sample(range(cluster_size), num_items_perturbed)
    return items_perturbed


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
    :return: delta
    """
    # exit if cluster is empty to avoid errors
    if len(cluster) == 0:
        return delta
    # choose a tag to remove from the cluster
    tag = random.choice(get_cluster_tags(cluster))
    # decide exactly which items will be perturbed
    items_perturbed = get_items_to_remove(cluster, random_percent, percent_removed)
    # iterate through the items to be perturbed
    for index in items_perturbed:
        # if the tag is in fact in the item
        if cluster[index][tag] != 0 and not has_only_one_tag(cluster[index]):
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


def remove_tag_from_data(data, item, tag):
    """
    removes a specified tag from an item in data
    :param data: the problem in list format
    :param item: the item number of the desired removal
    :param tag: the tag that should be removed
    :return: the perturbed dataset
    """
    # remove the tag from the specified item
    data[item][tag + 1] = 0
    return data


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
    data = remove_tag_from_data(data, item, tag)
    # output the file
    output_file_from_data(data, dataset_name, 0)


def random_all_clusters(filepath, percent_removed, number_generated, random_percent):
    """
    the main function that generates several perturbed data sets
    :param filepath: the file path of the dataset
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param number_generated: the number of perturbed datasets to generate
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
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
        random_all_clusters_internal(filepath, percent_removed, i, random_percent, dataset_name)


def random_all_clusters_internal(filepath, percent_removed, iteration_number, random_percent, dataset_name):
    """
    perturbs a dataset by removing a tag
    :param filepath: the file path of the dataset
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param iteration_number: the number that should be added to the end of the file's name when generated
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
    :param dataset_name: the name of the dataset
    :return: void
    """
    # parse the dataset
    data = parse_dataset(filepath)

    # use variables to point to parameters in the output file
    n, K, N, alpha, beta = return_parameters(data)

    # convert data into clustered
    clusters, cluster_index = convert_clusters(data)

    # create an empty string
    delta = ""
    # generate the deltas based on the removed tags
    delta = remove_all_random(clusters, percent_removed, random_percent, cluster_index, N, delta)

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write to the deltas file
        f.write(delta)
    print("------------------")

    # generate the output file for the perturbed dataset
    output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


def remove_all_random(clusters, percent_removed, random_percent, cluster_index, N, delta):
    """
    a helper function that removes a random tag from every cluster
    :param clusters: a list of clusters
    :param percent_removed: the percent of items that should be perturbed (0-100)
    :param random_percent: a boolean that causes the percent_removed to be ignored if true and instead uses a random percent
    :param cluster_index: a list that tracks the item numbers of items in the cluster list
    :param N: the parameter N of the problem
    :param delta: a string that will contain the changed tags and their strings
    :return: delta
    """
    # for each cluster
    for i, cluster in enumerate(clusters):
        # remove a single random tag to the cluster
        delta = remove_single_random(N, cluster, random_percent, percent_removed, cluster_index, delta, i)
    return delta

