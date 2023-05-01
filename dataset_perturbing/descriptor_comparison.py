"""descriptor_comparison.py: contains methods for comparing the minimum descriptors of datasets and plotting"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

import os
import re

import scipy as scipy
from matplotlib import pyplot as plt
import matplotlib.colors
import numpy as np
import scipy
import csv
from colour import Color

import ILP_linear as ilp_solve
from perturb_utilities import *


def find_descriptors(directory):
    """
    find the descriptors of the datasets in the given directory
    :param directory: the name of the directory within perturb_data
    :return: void
    """
    # generate a list of the files to test
    test_files = os.listdir(f"perturb_data/{directory}/")
    delta_files = os.listdir(f"perturb_data/{directory}_delta/")
    # sort the lists to ensure they are properly matched
    test_files.sort()
    delta_files.sort()
    # create an empty list of solutions
    solutions = []
    # for each data set
    for file in test_files:
        # add each solution to the solutions array
        solutions.append(ilp_solve.ILP_linear(f"perturb_data/{directory}/{file}"))

    # create an empty list of deltas
    deltas_text = ["" for i in range(len(delta_files) + 1)]
    # for each delta
    for i, file in enumerate(delta_files):
        # open the file
        with open(f"perturb_data/{directory}_delta/{file}") as f:
            # read the file
            deltas_text[i+1] = f.read()

    # create an empty list of deltas
    deltas = []
    # for each delta set
    for delta in deltas_text:
        # split on new line, remove the empty character at the end of the list
        deltas_temp = delta.split("\n")[:-1]
        # for each delta
        for i, d in enumerate(deltas_temp):
            # if the delta length is greater than 0
            if len(d) != 0:
                # split the lines on commas
                deltas_temp[i] = [int(number) for number in d.split(", ")]
        # append the list of deltas, remove last index because it is always empty
        deltas.append(deltas_temp)

    # create an empty list of sets of descriptors
    descriptors = []
    # for each descriptor set
    for s in solutions:
        # append the string form of each descriptor set to the list of descriptor sets
        descriptors.append(string_descriptor_to_array(s))

    # generate a list of the sizes of each explanation
    exp_sizes = [sum([len(descriptors[i][j]) for j in range(len(descriptors[i]))])
                         for i in range(len(descriptors))][1:]

    tag_changes_count = []
    changes_count = []

    # for each descriptor set
    for i, exp_size in enumerate(exp_sizes):
        # skip the first descriptor set because it will not be different from itself
        tags_added = len(deltas[i])
        # add the added tags to the list of tags added
        tag_changes_count.append(tags_added)
        # add the explanation size to the list of changes
        changes_count.append(exp_size)

    # write the data to a csv file
    write_data(directory, tag_changes_count, changes_count)
    # generate the graph corresponding to the data generated
    plot_tag_vs_explanation(directory)


def write_data(directory, tag_count, exp_sizes):
    """
    Write data generated from descriptor comparison to a csv file
    :param directory: the name of the directory that was tested
    :param tag_count: the array containing the number of tags added
    :param exp_sizes: the array containing the sizes of explanations
    :return: void
    """
    with open(f"perturb_data/csv/{directory}.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # f"Tags added/removed for {directory}"
        # f"Cluster Changes for {directory}"
        for (i, tag) in enumerate(tag_count):
            datawriter.writerow([tag, exp_sizes[i]])


def plot_tag_vs_explanation(directory):
    """
    a helper function that plots the graph of descriptor changes over tag additions
    :param directory: the name of the directory that was parsed
    :return: void
    """
    # create lists to store the data read from the directory
    tag_change_count = []
    changes_count = []

    with open(f"perturb_data/csv/{directory}.csv") as f:
        datareader = csv.reader(f, delimiter=",", quotechar="|")
        for row in datareader:
            tag_change_count.append(int(row[0]))
            changes_count.append(int(row[1]))

    # average cluster size
    avg_cluster_size = {t: [0, 0] for t in tag_change_count}
    for (i, t) in enumerate(tag_change_count):
        avg_cluster_size[t][0] += changes_count[i]
        avg_cluster_size[t][1] += 1

    for t in avg_cluster_size.keys():
        avg_cluster_size[t] = avg_cluster_size[t][0] / avg_cluster_size[t][1]

    tag_change_count = list(avg_cluster_size.keys())
    changes_count = list(avg_cluster_size.values())

    # label the two axes
    plt.ylabel("Average Explanation Size", rotation=90)
    plt.xlabel("Tags Added/Removed", rotation=0)

    # plot the points of each run of the graph as a
    # function of reduction in overall solution size over number of tags added
    plt.scatter(tag_change_count, changes_count, color="#91e2f6", zorder=2)

    # calculate the slope and y-intercept of the line of best fit
    m, b, r_value, p_value, std_err = scipy.stats.linregress(tag_change_count, changes_count)
    # generate an array of 120 evenly spaced samples of horizontal values
    x = np.linspace(min(tag_change_count), max(tag_change_count), 120)
    # plot the line of best fit
    plt.plot(x, m * x + b, "#8853a6", 2.5, zorder=1)

    # use the following calculations to calculate the bounds of the graph
    upper_x = max(tag_change_count) + 0.15 * (max(tag_change_count) - min(tag_change_count))
    lower_x = min(tag_change_count) - 0.15 * (max(tag_change_count) - min(tag_change_count))
    upper_y = max(changes_count) + 0.15 * (max(changes_count) - min(changes_count))
    lower_y = min(changes_count) - 0.15 * (max(changes_count) - min(changes_count))

    # print the r value of the line of best fit
    print(f"R value: {r_value}")
    # store the length of changes_count for use as shorthand in the calculation for the test statistic
    n = len(changes_count)
    # calculate the test statistic, or set it to a very high number if the r value is 1 or -1 to avoid division by zero
    test_stat = (r_value * ((n-2)**0.5)) / ((1 - (r_value ** 2))**0.5) if abs(r_value) != 1.0 else 10000.0
    # print the value of the test statistic
    print(f"Test statistic: {test_stat}")
    # print the
    print(f"P-value: {scipy.stats.norm.sf(abs(test_stat)) * 2}")

    # set the bounds of the graph
    plt.xlim([lower_x, upper_x])
    plt.ylim([lower_y, upper_y])

    # save a new image in the dataset's images folder
    plt.savefig(f"perturb_data/{directory}_images/"
                f"{directory}_{len(os.listdir(f'perturb_data/{directory}_images/'))}.png")

    # show the plot
    plt.show()
