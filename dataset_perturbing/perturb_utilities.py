"""perturb_utilities.py: A set of helper functions for perturbing datasets"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"


import random, math, os, shutil, re


def mat2_row_sum(matrix):
    """
    a helper function that sums the rows of a 2-dimensional list; do not use with lists of differing lengths
    :param matrix: a 2d matrix (list of lists with uniform length)
    :return: a list containing the sum of all rows in the input matrix
    """
    if len(matrix) != 0:
        row_sum = [0 for i in range(len(matrix[0]))]

        for row in matrix:
            for i, number in enumerate(row):
                row_sum[i] += number
        return row_sum
    else:
        return [0]


def find_most_used_tag(cluster):
    """
    a helper function to find the most used tag in a cluster
    :param cluster: a cluster in list of lists form
    :return: the tag that is used most frequently in the cluster
    """
    row_sum = mat2_row_sum(cluster)
    print(row_sum.index(max(row_sum)))
    return row_sum.index(max(row_sum))


def parse_dataset(filepath):
    """
    a helper function that converts a synthetic data file into list form
    :param filepath: the path to the file being parsed
    :return: void
    """
    # open the dataset
    with open(filepath) as dataset:
        file_in = dataset.read()

    # split the input on new lines
    rows = file_in.split("\n")
    # create an empty data array
    data = []
    # for each row in the input
    for row in rows:
        # split the data on spaces to form columns, cast to integer as well
        data.append([int(tag) for tag in row.split()])

    return data


def convert_clusters(data):
    """
    a helper function that converts input data into clustered form
    :param data: the list form of a dataset
    :return: a list of lists of items in clusters within the dataset
    """
    # create an empty list of lists containing each item in the cluster at index i
    clusters = [[] for i in range(data[0][1] + 1)]
    # create an empty list of lists of the same size as the previous list
    cluster_index = [[] for i in range(data[0][1] + 1)]
    # for each cluster
    for i in range(1, data[0][0] + 1):
        # append the item in the cluster (formatted as such to avoid issues with ordering)
        #                                (the 2 is to exclude the item number and cluster number)
        clusters[int(data[i][1])].append(data[i][2:])
        # append the item number to the index list
        cluster_index[int(data[i][1])].append(data[i][0])
    return clusters, cluster_index


def setup_directories(filepath):
    """
    a helper function that sets up the required directories for a given perturbing test,
    then returns the name of the dataset based on what the file is called
    :param filepath: the path to the dataset
    :return: void, creates directories in the perturb_data folder
    """
    # find the name of the dataset using a regular expression
    dataset_name = re.findall(r'(?<=test_txt_files\/).*?(?=\.txt)', filepath)[0]

    # if the path to the testing folder does not exist, create the necessary directories
    if not os.path.exists(f"perturb_data/{dataset_name}/"):
        # create directory
        os.makedirs(f"perturb_data/{dataset_name}/")

    # if the path to the testing folder does not exist, create the necessary directories
    if not os.path.exists(f"perturb_data/{dataset_name}_delta/"):
        # create directory
        os.makedirs(f"perturb_data/{dataset_name}_delta/")

    # if the path to the testing folder does not exist, create the necessary directories
    if not os.path.exists(f"perturb_data/{dataset_name}_images/"):
        # create directory
        os.makedirs(f"perturb_data/{dataset_name}_images/")

    # copy the original file to the perturb testing directory
    shutil.copy(filepath, f"perturb_data/{dataset_name}/")

    return dataset_name


def return_parameters(data):
    """
    a helper function that returns the n, K, N, alpha, and beta values of the set
    :param data: a dataset in list format
    :return: the parameters n, K, N, alpha, and beta
    """
    return data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]


def output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number):
    """
    a helper function that generates an output file from a set of data
    :param n: n
    :param K: K
    :param N: N
    :param alpha: alpha
    :param beta: beta
    :param clusters: a list of clusters and the items they contain
    :param dataset_name: the name of the dataset
    :param iteration_number: the current iteration number
    :return: void
    """
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
    with open(f"perturb_data/{dataset_name}/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)


def output_file_from_data(data, dataset_name, iteration_number):
    """
    uses a dataset in list format to generate an output file
    :param data: a dataset in list format
    :param dataset_name: the name of the dataset
    :param iteration_number: the number that should be appended to the end of the filename
    :return: void
    """
    output_string = ""
    for row in data:
        for column in row:
            output_string += f"{column} "
        output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"perturb_data/{dataset_name}/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)


def get_cluster_tags(cluster):
    """
    a helper function to get all tags used within a cluster
    :param cluster: a cluster in list form
    :return: a list of tags that are used within the dataset (indexing at 0)
    """
    tags = []
    for item in cluster:
        for i, tag in enumerate(item):
            if tag == 1 and i not in tags:
                tags.append(i)
    return tags


def get_items_to_perturb(cluster, random_percent, percent_added):
    """
    a helper function that returns a list of items to perturb
    :param cluster: a cluster in list form
    :param random_percent: a boolean determining whether the percent of items perturbed is random
    :param percent_added: a percent (0-100) of the items in the cluster that should be perturbed
    :return: a list of items to be perturbed
    """
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
    return items_perturbed