# William Bradford
# wcb8ze
# contains utilities for perturbing data sets

import random, math, os, shutil, re


def parse_dataset(filepath):
    """
    a helper function that converts a synthetic data file into list form
    :param filepath: the path to the file being parsed
    :return:
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


#
# parameters:
#       - data: the parsed input of a data set
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


# a helper function that returns the n, K, N, alpha, and beta values of the set
# parameters:
#       - data
def return_parameters(data):
    return data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]


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
def output_file_from_clusters(n, K, N, alpha, beta, clusters, dataset_name, iteration_number):
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
    output_string = ""
    for row in data:
        for column in row:
            output_string += f"{column} "
        output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"perturb_data/{dataset_name}/{dataset_name}_{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(output_string)