# William Bradford
# wcb8ze
# contains methods for perturbing datasets

# this file includes imports of random, math, os, and shutil
from perturb_utilities import *


# a helper function that adds a random tag to every cluster
# parameters:
#       - clusters: a list of clusters
#       - percent_added: the percent of items in the cluster that should be added
#       - random_percent: a boolean that allows the previous parameter to be ignored in favor of a random percentage
#       - cluster_index: a list that tracks what item number an item within a cluster is
#       - N: the N value of the overall problem
#       - delta: a string that will contain the changed tags and their item numbers
def add_all_random(clusters, percent_added, random_percent, cluster_index, N, delta):
    # for each cluster
    for i, cluster in enumerate(clusters):
        # add a single random tag to the cluster
        delta = add_single_random(N, cluster, random_percent, percent_added, cluster_index, delta, i)
    return delta


# a helper function that adds a random tag to a single cluster
# parameters:
#       - clusters: a list of clusters
#       - percent_added: the percent of items in the cluster that should be added
#       - random_percent: a boolean that allows the previous parameter to be ignored in favor of a random percentage
#       - cluster_index: a list that tracks what item number an item within a cluster is
#       - N: the N value of the overall problem
#       - delta: a string that will contain the changed tags and their item numbers
#       - current_cluster: an int that tracks the cluster that is being perturbed
def add_single_random(N, cluster, random_percent, percent_added, cluster_index, delta, current_cluster):
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
        if cluster[index][tag] != 1:
            # add the tag
            cluster[index][tag] = 1
            print(f"added tag {tag + 1} in item {index} of cluster {current_cluster}, item "
                  f"{cluster_index[current_cluster][index]}")
            # note which data item was given which tag
            delta += f"{cluster_index[current_cluster][index]}, {tag + 1} \n"
    return delta


# a helper function that generates an output file from a set of data
# parameters:
#       - n
#       - K
#       - N
#       - alpha
#       - beta
#       - clusters: a list of clusters and the items they contain
#       - dataset_name: the name of the dataset
#       - iteration_number: the current iteration number
def output_file(n, K, N, alpha, beta, clusters, dataset_name, iteration_number):
    # generate the first line of the output file
    output_string = f"{n} {K} {N} {alpha} {beta} \n"
    # use a temporary counter
    item_number = 1
    # for each cluster
    for i in range(0, len(clusters)):
        # for each item in the cluster
        for item in clusters[i]:
            # add the item number and cluster to that line
            output_string += f"{item_number} {i} "
            # increment item_number
            item_number += 1
            for tag in item:
                # add each tag
                output_string += f"{tag} "
            # add a new line to the output string
            output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"perturb_testing/{dataset_name}/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)


# a helper function that returns the n, K, N, alpha, and beta values of the set
# parameters:
#       - data
def return_parameters(data):
    return data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]


# perturbs a dataset by adding a tag
# parameters:
#       - filepath: a path to the perturbed file being converted
#       - percent_added: the percent of items in each cluster that will be perturbed
#       - iteration_number: the number of the current iteration (for text file generation purposes)
#       - random_percent: adds a tag to a random number of items in a cluster if true
def random_all_clusters_internal(filepath, percent_added, iteration_number, random_percent, dataset_name):

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
    with open(f"perturb_testing/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write to the deltas file
        f.write(delta)
    print("------------------")

    # generate the output file for the perturbed dataset
    output_file(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)


# the main function that generates several perturbed data sets
# parameters:
#       - filepath: the path to the file to perturb
#       - percent_added: the percentage of each cluster that is to be perturbed
#       - number_generated: the number perturbed datasets to be generated
#       - random_percent: adds a tag to a random number of items within each cluster
def random_all_clusters(filepath, percent_added, number_generated, random_percent):
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


# perturb a single cluster, use a random amount of tags
def random_single_cluster(filepath, percent_added, number_generated, random_percent, cluster):
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


# helper function to perturb a single cluster with a random amount of tags
def random_single_cluster_internal(filepath, percent_added, iteration_number, random_percent, dataset_name, cluster):

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
    with open(f"perturb_testing/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

    # generate the final output file of the perturbed data set
    output_file(n, K, N, alpha, beta, clusters, dataset_name, iteration_number)

#applying functions to example txt files
random_all_clusters_internal("test_txt_files/4x14.txt", 50, 1, True, "test_txt_files/4x14.txt")
print("--------------------------------------------")
random_all_clusters("test_txt_files/4x14.txt", 80, 2, 50)
print("--------------------------------------------")
random_single_cluster_internal("test_txt_files/4x14.txt", 50, 1, 50, 1)
