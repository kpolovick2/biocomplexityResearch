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

    plot_tag_vs_explanation(tag_changes_count, changes_count, directory)


def plot_tag_vs_explanation(tag_change_count, changes_count, directory):
    """
    a helper function that plots the graph of descriptor changes over tag additions
    :param tag_change_count: a list that contains the tags added and
    corresponds to the indexes to changes_count
    :param changes_count: a list that contains the change in descriptor size
    and corresponds to the indexes of tags_added-count
    :param directory: the name of the directory
    :return: void
    """
    # generate a list of lists to store point frequencies
    point_frequency = [[0 for i in range(max(changes_count) + 1)]
                       for j in range(max(tag_change_count) + 1)]

    max_freq = 0
    # store the number of occurrences of each point
    for (i, tags) in enumerate(tag_change_count):
        # increment the value of the index in the array corresponding to each point
        point_frequency[tags][changes_count[i]] += 1
        # assign max_freq to the value of point_frequency if it is higher than the current max_freq
        max_freq = point_frequency[tags][changes_count[i]] \
            if point_frequency[tags][changes_count[i]] > max_freq \
            else max_freq

    # create an array to store the color values of points in the scatter plot
    # this works by looking up the frequencies of each point (stored in point_frequency)
    # and storing it in the index that corresponds to the point that has been looked up
    colors = [point_frequency[tags][changes_count[i]] for (i, tags) in enumerate(tag_change_count)]

    # generate a custom color map
    color_map = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#91e2f6", "#f527ed"])

    # label the two axes
    plt.ylabel("Cluster Size", rotation=90)
    plt.xlabel("Tags Added/Removed", rotation=0)

    # plot the points of each run of the graph as a
    # function of reduction in overall solution size over number of tags added
    plt.scatter(tag_change_count, changes_count, c=colors, cmap=color_map, zorder=2)

    # calculate the slope and y-intercept of the line of best fit
    m, b, r_value, p_value, std_err = scipy.stats.linregress(tag_change_count, changes_count)
    # generate an array of 120 evenly spaced samples of horizontal values
    x = np.linspace(min(tag_change_count), max(tag_change_count), 120)
    # plot the line of best fit
    plt.plot(x, m * x + b, "#8853a6", 2.5, zorder=1)
    # create and plot the color legend
    colorbar = plt.colorbar()
    # set the padding of the color legend
    colorbar.ax.get_yaxis().labelpad = 15
    # set the number of y ticks to be at 3, positioned at the bottom, middle, and top
    colorbar.ax.set_yticks([0.0, max_freq / 2, max_freq])
    # label the ticks low, medium, and high
    colorbar.ax.set_yticklabels(['Low', 'Medium', 'High'])
    # set the label of the color legend
    colorbar.set_label("Frequency of Change", rotation=270)

    # use the following calculations to calculate the bounds of the graph
    upper_x = max(tag_change_count) + 0.25
    lower_x = min(tag_change_count) - 0.25
    upper_y = max(changes_count) + 0.25
    lower_y = min(changes_count) - 0.25

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
        print(file)
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
                    print(f"Cluster {j+1} of dataset {i} shrinks by {abs(change)}")
                elif change < 0:
                    print(f"Cluster {j+1} of dataset {i} grows by {abs(change)}")
            print(f"The overall explanation size changes by {-signed_changes}")

            tags_removed_count.append(tags_removed)
            changes_count.append(-signed_changes)
    write_data(directory, tags_removed_count, changes_count)

def write_data(directory, tag_count, change_count):
    with open(f"perturb_data/{directory}.csv", "a") as f:
        datawriter = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        tag_count.insert(0, f"Tags added/removed for {directory}")
        datawriter.writerow(tag_count)
        change_count.insert(0, f"Cluster Changes for {directory}")
        datawriter.writerow(change_count)