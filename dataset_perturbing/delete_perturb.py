"""delete_perturb.py: contains methods for perturbing datasets by deleting tags"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

# this file includes imports of random, math, os, and shutil
from perturb_utilities import *

def remove_single_random(N, cluster, random_percent, percent_added, cluster_index, delta, current_cluster):
    # choose a tag to add to the cluster
    tag = random.choice(range(N))
    # find the number of items in the cluster
    cluster_size = len(cluster)
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
    # iterate through the items to be perturbed
    for index in items_perturbed:
        # if the tag is not already in the item
        if cluster[index][tag] != 0:
            # add the tag
            cluster[index][tag] = 0
            print(f"added tag {tag + 1} in item {index} of cluster {current_cluster}, item "
                  f"{cluster_index[current_cluster][index]}")
            # note which data item was given which tag
            delta += f"{cluster_index[current_cluster][index]}, {tag + 1} \n"
    return delta


def random_single_cluster_internal(filepath, percent_added, iteration_number, random_percent, dataset_name, cluster):
    """
    helper function to perturb a single cluster with a random amount of tags
    :param filepath:
    :param percent_added:
    :param iteration_number:
    :param random_percent:
    :param dataset_name:
    :param cluster:
    :return:
    """
    # parse the dataset
    data = parse_dataset(filepath)

    # use variables to point to parameters in the output file
    n, K, N, alpha, beta = return_parameters(data)

    # convert data into clustered
    clusters, cluster_index = convert_clusters(data)

    # generate the deltas based on the added tags
    delta = remove_single_random(N, clusters[cluster], random_percent, percent_added, cluster_index, "", cluster)

    # generate a deltas file
    with open(f"perturb_data/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

    # generate the final output file of the perturbed data set
    output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


# perturb a single cluster, use a random amount of tags
def random_single_cluster(filepath, percent_removed, number_generated, random_percent, cluster):
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