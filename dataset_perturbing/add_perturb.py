"""add_perturb.py: a set of functions for perturbing a dataset by adding tags"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

# this file includes imports of random, math, os, and shutil
from perturb_utilities import *


def add_all_random(clusters, percent_added, random_percent, cluster_index, N, delta):
    """
    a helper function that adds a random tag to every cluster
    :param clusters: a list of clusters
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param cluster_index: a list that tracks the item numbers of items in the cluster list
    :param N: the parameter N of the problem
    :param delta: a string that will contain the changed tags and their strings
    :return: void
    """
    # for each cluster
    for i, cluster in enumerate(clusters):
        # add a single random tag to the cluster
        delta = add_single_random(N, cluster, random_percent, percent_added, cluster_index, delta, i)
    return delta


def add_single_random(N, cluster, random_percent, percent_added, cluster_index, delta, current_cluster):
    """
    a helper function that adds a random tag to a single cluster
    :param N: the parameter N of the problem
    :param cluster: a list containing data from each item of a cluster
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param cluster_index: a list that tracks the item numbers of items in the cluster list
    :param delta: a string that will contain the changed tags and their strings
    :param current_cluster: an int that tracks the cluster that is being perturbed
    :return:
    """
    # choose a tag to add to the cluster
    tag = random.choice(range(N))
    # find the number of items in the cluster
    cluster_size = len(cluster)
    # decide exactly which items will be perturbed
    items_perturbed = get_items_to_perturb(cluster, random_percent, percent_added)
    # iterate through the items to be perturbed
    for index in items_perturbed:
        # if the tag is not already in the item
        if cluster[index][tag] != 1:
            # add the tag
            cluster[index][tag] = 1
            print(f"added tag {tag + 1} in item {index} of cluster {current_cluster}, item "
                  f"{cluster_index[current_cluster][index]}")
            # note which data item was given which tag
            delta += f"{cluster_index[current_cluster][index]}, {tag + 1} \n"
    return delta


#
# parameters:
#       - filepath: a path to the perturbed file being converted
#       - percent_added: the percent of items in each cluster that will be perturbed
#       - iteration_number: the number of the current iteration (for text file generation purposes)
#       - random_percent: adds a tag to a random number of items in a cluster if true
def random_all_clusters_internal(filepath, percent_added, iteration_number, random_percent, dataset_name):
    """
    perturbs a dataset by adding a tag
    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param iteration_number: the number that should be added to the end of the file's name when generated
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
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
    # generate the deltas based on the added tags
    delta = add_all_random(clusters, percent_added, random_percent, cluster_index, N, delta)

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write to the deltas file
        f.write(delta)
    print("------------------")

    # generate the output file for the perturbed dataset
    output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


def random_all_clusters(filepath, percent_added, number_generated, random_percent):
    """
    the main function that generates several perturbed data sets
    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param number_generated: the number of perturbed datasets to generate
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
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
        random_all_clusters_internal(filepath, percent_added, i, random_percent, dataset_name)


def random_single_cluster(filepath, percent_added, number_generated, random_percent, cluster):
    """
    perturbs a single cluster, use a random amount of tags
    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param number_generated: the number of perturbed datasets to generate
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
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
        random_single_cluster_internal(filepath, percent_added, i, random_percent, dataset_name, cluster)


def random_single_cluster_internal(filepath, percent_added, iteration_number, random_percent, dataset_name, cluster):
    """
    helper function to perturb a single cluster with a random amount of tags
    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param iteration_number: the number that should be added to the end of the file's name when generated
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param dataset_name: the name of the dataset
    :param cluster: the cluster to be perturbed
    :return: void
    """
    # parse the dataset
    data = parse_dataset(filepath)

    # use variables to point to parameters in the output file
    n, K, N, alpha, beta = return_parameters(data)

    # convert data into clustered
    clusters, cluster_index = convert_clusters(data)

    # create an empty delta string
    delta = ""
    # generate the deltas based on the added tags
    delta = add_single_random(N, clusters[cluster], random_percent, percent_added, cluster_index, delta, cluster)

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

    # generate the final output file of the perturbed data set
    output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


def add_tag_to_item(filepath, item, tag):
    """
    Adds one tag to one item in a dataset
    :param filepath: the file path of the dataset
    :param item: the item to be perturbed
    :param tag: the tag to be added
    :return void
    """
    # set up the output directories if they are not already set up
    dataset_name = setup_directories(filepath)
    # parse the input dataset
    data = parse_dataset(filepath)
    # add the tag to the specified item
    data[item][tag + 1] = 1
    # output the file
    output_file_from_data(data, dataset_name, 0)