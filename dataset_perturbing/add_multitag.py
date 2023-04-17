"""add_multitag.py: a set of functions for perturbing a dataset by adding multiple tags"""
__author__ = "William Bradford, Keara Polovick"
__email__ = "wcb8ze@virginia.edu"

from perturb_utilities import *


def multitag_random_single_cluster(
    filepath, percent_added, number_generated, random_percent,
        bottom_cluster, top_cluster, lowest_tagcount, highest_tagcount
):
    """
    perturb a random amount of items in a cluster by adding num_tags tags

    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param number_generated: the number of perturbed datasets to generate
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param bottom_cluster:
    :param top_cluster:
    :param lowest_tagcount:
    :param highest_tagcount:
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
    for i in range(bottom_cluster, top_cluster + 1):
        for j in range(lowest_tagcount, highest_tagcount + 1):
            # generation function
            __multitag_random_single_cluster_internal(
                filepath, percent_added, i * (highest_tagcount - lowest_tagcount) + j, random_percent, dataset_name, i, j
        )


def __multitag_random_single_cluster_internal(
    filepath,
    percent_added,
    iteration_number,
    random_percent,
    dataset_name,
    cluster,
    num_tags,
):
    """
    helper function to perturb a random selection of items from a single cluster by adding num_tags tags
    :param filepath: the file path of the dataset
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param iteration_number: the number that should be added to the end of the file's name when generated
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param dataset_name: the name of the dataset
    :param cluster: the cluster to be perturbed
    :param num_tags: the number of tags that should be added to each item
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
    delta = add_multiple_random(
        N,
        clusters[cluster],
        random_percent,
        percent_added,
        cluster_index,
        delta,
        cluster,
        num_tags,
    )

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

    # generate the final output file of the perturbed data set
    output_file_from_clusters(
        n, K, N, alpha, beta, clusters, dataset_name, iteration_number
    )


def add_multiple_random(
    N,
    cluster,
    random_percent,
    percent_added,
    cluster_index,
    delta,
    current_cluster,
    num_tags,
):
    """
    a helper function that adds num_tags random tags to a single cluster
    :param N: the parameter N of the problem
    :param cluster: a list containing data from each item of a cluster
    :param random_percent: a boolean that causes the percent_added to be ignored if true and instead uses a random percent
    :param percent_added: the percent of items that should be perturbed (0-100)
    :param cluster_index: a list that tracks the item numbers of items in the cluster list
    :param delta: a string that will contain the changed tags and their strings
    :param current_cluster: an int that tracks the cluster that is being perturbed
    :param num_tags: an int that specifies the number of tags to be added
    :return: delta: a list representing which tags were added to which items
    """
    # choose a tag to add to the cluster
    tags = random.sample(range(N), num_tags)
    # find the number of items in the cluster
    cluster_size = len(cluster)
    # decide exactly which items will be perturbed
    items_perturbed = get_items_to_perturb(
        cluster, random_percent, percent_added)
    # iterate through the items to be perturbed
    for index in items_perturbed:
        for tag in tags:
            # if the tag is not already in the item
            if cluster[index][tag] != 1:
                # add the tag
                cluster[index][tag] = 1
                print(
                    f"added tag {tag + 1} in item {index} of cluster {current_cluster}, item "
                    f"{cluster_index[current_cluster][index]}"
                )
                # note which data item was given which tag
                delta += f"{cluster_index[current_cluster][index]}, {tag + 1} \n"
    return delta
