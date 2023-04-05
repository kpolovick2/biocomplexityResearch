# William Bradford
# wcb8ze
# contains methods for perturbing datasets

import random, math, os, shutil

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
        # split the data on spaces
        data.append(row.split())

    # for each row in data
    for row in data:
        # split the data on spaces to get tags
        for i in range(len(row)):
            row[i] = int(row[i])

    return data


def generate_deltas(clusters, percent_added, random_percent, cluster_index, N):
    delta = ""
    # for each cluster
    for i, cluster in enumerate(clusters):
        # choose a tag to add to the cluster
        tag = random.choice(range(N))
        # find the number of items in the cluster
        cluster_size = len(cluster)
        # perturb at most percent_added percent of the cluster
        if cluster_size == 0:
            num_items_perturbed = 0
        elif random_percent:
            num_items_perturbed = random.choice(range(1, cluster_size + 1))
        else:
            num_items_perturbed = math.floor(percent_added / 100 * cluster_size)
        # decide which items will be perturbed
        items_perturbed = random.sample(range(cluster_size), num_items_perturbed)
        # iterate through the items to be perturbed
        for index in items_perturbed:
            # add the tag
            cluster[index][tag] = 1
            print(f"added tag {tag + 1} in item {index} of cluster {i}, item {cluster_index[i][index]}")
            delta += f"{cluster_index[i][index]}, {tag + 1} \n"
    return delta


# perturbs a dataset by adding a tag
# parameters:
#       - filepath: a path to the perturbed file being converted
#       - percent_added: the percent of items in each cluster that will be perturbed
#       - iteration_number: the number of the current iteration (for text file generation purposes)
#       - random_percent: adds a tag to a random number of items in a cluster if true
def random_all_clusters_internal(filepath, percent_added, iteration_number, random_percent, dataset_name):

    data = parse_dataset(filepath)

    # assign parameters
    n = int(data[0][0])
    K = int(data[0][1])
    N = int(data[0][2])
    alpha = data[0][3]
    beta = data[0][4]

    # create a list of lists containing each item in the cluster at index i
    clusters = [[] for i in range(K + 1)]
    # for each cluster
    cluster_index = [[] for i in range(K+1)]
    for i in range(1, n + 1):
        # append the item in the cluster (formatted as such to avoid issues with ordering)
        #                                (the 2 is to exclude the item number and cluster number)
        clusters[int(data[i][1])].append(data[i][2:])
        cluster_index[int(data[i][1])].append(data[i][0])

    # generate the deltas based on the added tags
    delta = generate_deltas(clusters, percent_added, random_percent, cluster_index, N)

    # generate a deltas file
    with open(f"perturb_testing/{dataset_name}_delta/{iteration_number}.txt", "w") as f:
        # write the output file
        f.write(delta)
    print("------------------")

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

    # ------------------------------------
    # execution section
    # ------------------------------------
    # generate number_generated perturbed datasets
    for i in range(1, number_generated + 1):
        # generation function
        random_all_clusters_internal(filepath, percent_added, i, random_percent, dataset_name)


def random_single_cluster(filepath, percent_added, iteration_number, random_percent, dataset_name, cluster):
    # open the dataset
    with open(filepath) as dataset:
        file_in = dataset.read()

    # split the input on new lines
    rows = file_in.split("\n")
    # create an empty data array
    data = []
    # for each row in the input
    for row in rows:
        # split the data on spaces
        data.append(row.split())

    # for each row in data
    for row in data:
        # split the data on spaces to get tags
        for i in range(len(row)):
            row[i] = int(row[i])

    # assign parameters
    n = int(data[0][0])
    K = int(data[0][1])
    N = int(data[0][2])
    alpha = data[0][3]
    beta = data[0][4]


