# William Bradford
# wcb8ze
# contains utilities for perturbing data sets

import random, math, os, shutil


# a helper function that converts a synthetic data file into list form
# paramters:
#       - filepath: the path to the file being parsed
def parse_dataset(filepath):
    # open the dataset
    with open(filepath) as dataset:
        file_in = dataset.read()

    # split the input on new lines
    rows = file_in.split("\n")
    # create an empty data array
    data = []
    # for each row in the input
    for row in rows:
        # split the data on spaces to form columns
        data.append(row.split())

    # for each row in data
    for row in data:
        # for each number in the row
        for i in range(len(row)):
            # cast the number to an int (from a string)
            row[i] = int(row[i])

    return data


# a helper function that converts input data into clustered form
# parameters:
#       - data: the parsed input of a data set
def convert_clusters(data):
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


# a helper function that sets up the required directories for a given perturbing test,
# then returns the name of the dataset based on what the file is called
# parameters:
#       - filepath: the path to the dataset
def setup_directories(filepath):
    # split the filepath to get the name of the dataset
    filepath_split = filepath.split("/")
    # find the name of the dataset
    dataset_name = filepath_split[len(filepath_split) - 1].split(".")[0]

    # if the path to the testing folder does not exist, create the necessary directories
    if not os.path.exists(f"perturb_testing/{dataset_name}/"):
        # create directory
        os.makedirs(f"perturb_testing/{dataset_name}/")

    # if the path to the testing folder does not exist, create the necessary directories
    if not os.path.exists(f"perturb_testing/{dataset_name}_delta/"):
        # create directory
        os.makedirs(f"perturb_testing/{dataset_name}_delta/")

    # copy the original file to the perturb testing directory
    shutil.copy(filepath, f"perturb_testing/{dataset_name}/")

    return dataset_name
