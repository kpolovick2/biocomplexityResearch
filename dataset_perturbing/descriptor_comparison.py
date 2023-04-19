"""descriptor_comparison.py: contains methods for comparing the minimum descriptors of datasets and plotting"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

import os
import re

import scipy as scipy
from matplotlib import pyplot as plt
import numpy as np
import scipy

import ILP_linear as ilp_solve


def string_descriptor_to_array(D):
    """
    takes in a descriptor set D and converts it into an array of arrays of integers
    :param D: a list of descriptors (a descriptor set)
    :return: void
    """
    # create an empty list of descriptors
    descriptors = []
    # split the descriptors
    y_values = D.split("\n")
    # for each descriptor in the set
    for y in y_values:
        # ensure that the line being interpreted is actually a descriptor
        if len(y) != 0 and y[0] == "D":
            # use a regular expression to find all the tags
            d_re = re.findall(r'(?<=\[).*?(?=\])', y)
            # split the tags into a list
            descriptor = d_re[0].split(", ")
            # add the list in array form to the array of arrays
            descriptors.append([
                int(tag) for tag in descriptor])

    return descriptors


def find_descriptors_added(directory):
    """
    find the descriptors of the datasets in the given directory
    :param directory: the name of the directory within perturb_data
    :return: void
    """
    # generate a list of the files to test
    test_files = os.listdir(f"perturb_data/{directory}/")
    delta_files = os.listdir(f"perturb_data/{directory}_delta/")
    # create an empty list of solutions
    solutions = []
    # for each data set
    for file in test_files:
        # add each solution to the solutions array
        solutions.append(ilp_solve.ILP_linear(f"perturb_data/{directory}/{file}"))

    # create an empty list of deltas
    deltas_text = ["" for i in range(len(delta_files))]
    # for each delta
    for i, file in enumerate(delta_files):
        # open the file
        with open(f"perturb_data/{directory}_delta/{file}") as f:
            # read the file
            deltas_text[i] = f.read()

    # create an empty list of deltas
    deltas = []
    # for each delta set
    for delta in deltas_text:
        # split on new line
        deltas_temp = delta.split("\n")
        # for each delta
        for i, d in enumerate(deltas_temp):
            # if the delta length is greater than 0
            if len(d) != 0:
                # split the lines on commas
                deltas_temp[i] = [int(number) for number in d.split(", ")]
        # append the list of deltas, remove last index because it is always empty
        deltas.append(deltas_temp[:len(deltas_temp)-1])

    # create an empty list of sets of descriptors
    descriptors = []
    # for each descriptor set
    for s in solutions:
        # append the string form of each descriptor set to the list of descriptor sets
        descriptors.append(string_descriptor_to_array(s))

    # generate a list of the sizes of each descriptor
    descriptor_sizes = [[len(descriptors[i][j]) for j in range(len(descriptors[i]))] for i in range(len(descriptors))]

    # copy the elements of descriptor_sizes at i > 0, then take the difference
    # between those rows and the first row of descriptor_sizes to obtain the change in sizes
    change_size = [[item - descriptor_sizes[0][j] for j, item in enumerate(size)] for size in descriptor_sizes]

    # copy the descriptors list and call it diff
    # this is done in this manner because it copies the memory address of the internal lists we use descriptors.copy()
    # diff = [[descriptors[i][j].copy() for j in range(len(descriptors[i]))] for i in range(len(descriptors))]
    # # for each descriptor set in the set of descriptor sets
    # for i, descriptor_set in enumerate(descriptors):
    #     # for descriptor in the descriptor set
    #     for j, descriptor in enumerate(descriptor_set):
    #         # for each tag in the descriptor
    #         for k, tag in enumerate(descriptor):
    #             # cast to an int
    #             descriptors[i][j][k] = tag
    #             # set the value in the diff array to the difference between the two tags
    #             diff[i][j][k] = descriptors[0][j][k] - descriptors[i][j][k]

    tags_added_count = []
    changes_count = []

    # for each descriptor set
    for i, descriptor_set in enumerate(change_size):
        # skip the first descriptor set because it will not be different from itself
        if i != 0:
            print("-------------------\nAddition(s) to the dataset:")
            # print which tags were added to the dataset
            for j, pair in enumerate(deltas[i-1]):
                print(f"Tag {pair[1]} added to item {pair[0]}")
            # store the number of tags added
            tags_added = len(deltas[i-1])
            print("Cluster changes:")
            # create a variable to store the total number of changes relative to the original dataset
            sum_changes = 0
            signed_changes = 0
            # print the changes in the cluster
            for j, change in enumerate(descriptor_set):
                sum_changes += abs(change)
                signed_changes += change
                if change > 0:
                    print(f"Cluster {j+1} of dataset {i} grows by {abs(change)}")
                elif change < 0:
                    print(f"Cluster {j+1} of dataset {i} shrinks by {abs(change)}")
            if signed_changes > 0:
                raise Exception(f"Some error caused this solution to grow larger. This occurred in data set {i}.")

            tags_added_count.append(tags_added)
            changes_count.append(sum_changes)
    plot_tag_additions(tags_added_count, changes_count, directory)


def plot_tag_additions(tags_added_count, changes_count, directory):
    """
    a helper function that plots the graph of descriptor changes over tag additions
    :param tags_added_count: a list that contains the tags added and
    corresponds to the indexes to changes_count
    :param changes_count: a list that contains the change in descriptor size
    and corresponds to the indexes of tags_added-count
    :param directory: the name of the directory
    :return: void
    """

    # plot the points of each run of the graph as a
    # function of reduction in overall solution size over number of tags added
    plt.plot(tags_added_count, changes_count, 'o', color='#EA9E8D')

    # calculate the slope and y-intercept of the line of best fit
    m, b, r_value, p_value, std_err = scipy.stats.linregress(tags_added_count, changes_count)
    # generate an array of 120 evenly spaced samples of horizontal values
    x = np.linspace(min(tags_added_count), max(tags_added_count), num=120)
    # plot the line of best fit
    plt.plot(x, m * x + b, color="#D64550", lw=2.5)
    # save a new image in the dataset's images folder
    plt.savefig(f"perturb_data/{directory}_images/"
                f"{directory}_{len(os.listdir(f'perturb_data/{directory}_images/'))}.png")

    # use the following calculations to calculate the bounds of the graph
    upper_x = max(tags_added_count) + 1
    lower_x = min(tags_added_count) - 1
    upper_y = max(changes_count) + 1
    lower_y = min(changes_count) - 1

    print(f"R value: {r_value}")
    n = len(changes_count)
    test_stat = (r_value * ((n-2)**0.5)) / ((1 - (r_value ** 2)**0.5))
    print(f"Test statistic: {test_stat}")

    plt.xlim([lower_x, upper_x])
    plt.ylim([lower_y, upper_y])
    # show the plot
    plt.show()


def find_descriptors_removed(directory):
    """
    find the descriptors of the datasets in the given directory, use when tags are removed
    :param directory: the name of the directory within perturb_data
    :return: void
    """
    # generate a list of the files to test
    test_files = os.listdir(f"perturb_data/{directory}/")
    delta_files = os.listdir(f"perturb_data/{directory}_delta/")
    # create an empty list of solutions
    solutions = []
    # for each data set
    for file in test_files:
        # add each solution to the solutions array
        solutions.append(ilp_solve.ILP_linear(f"perturb_data/{directory}/{file}"))

    # create an empty list of deltas
    deltas_text = ["" for i in range(len(delta_files))]
    # for each delta
    for i, file in enumerate(delta_files):
        # open the file
        with open(f"perturb_data/{directory}_delta/{file}") as f:
            # read the file
            deltas_text[i] = f.read()

    # create an empty list of deltas
    deltas = []
    # for each delta set
    for delta in deltas_text:
        # split on new line
        deltas_temp = delta.split("\n")
        # for each delta
        for i, d in enumerate(deltas_temp):
            # if the delta length is greater than 0
            if len(d) != 0:
                # split the lines on commas
                deltas_temp[i] = [int(number) for number in d.split(", ")]
        # append the list of deltas, remove last index because it is always empty
        deltas.append(deltas_temp[:len(deltas_temp)-1])

    # create an empty list of sets of descriptors
    descriptors = []
    # for each descriptor set
    for s in solutions:
        # append the string form of each descriptor set to the list of descriptor sets
        descriptors.append(string_descriptor_to_array(s))

    # generate a list of the sizes of each descriptor
    descriptor_sizes = [[len(descriptors[i][j]) for j in range(len(descriptors[i]))] for i in range(len(descriptors))]

    # copy the elements of descriptor_sizes at i > 0, then take the difference
    # between those rows and the first row of descriptor_sizes to obtain the change in sizes
    change_size = [[item - descriptor_sizes[0][j] for j, item in enumerate(size)] for size in descriptor_sizes]

    tags_removed_count = []
    changes_count = []

    # for each descriptor set
    for i, descriptor_set in enumerate(change_size):
        # skip the first descriptor set because it will not be different from itself
        if i != 0:
            print("-------------------\nRemoval(s) from the dataset:")
            # print which tags were removed from the dataset
            for j, pair in enumerate(deltas[i-1]):
                print(f"Tag {pair[1]} removed from item {pair[0]}")
            # store the number of tags removed
            tags_removed = len(deltas[i-1])
            print("Cluster changes:")
            # create a variable to store the total number of changes relative to the original dataset
            sum_changes = 0
            signed_changes = 0
            # print the changes in the cluster
            for j, change in enumerate(descriptor_set):
                sum_changes += abs(change)
                signed_changes += change
                if change > 0:
                    print(f"Cluster {j+1} of dataset {i} grows by {abs(change)}")
                elif change < 0:
                    print(f"Cluster {j+1} of dataset {i} shrinks by {abs(change)}")
            if signed_changes < 0:
                raise Exception(f"Some error caused this solution to shrink. This occurred in data set {i}.")

            tags_removed_count.append(tags_removed)
            changes_count.append(sum_changes)
    # plot_tag_additions(tags_removed_count, changes_count, directory)