# William Bradford
# wcb8ze
# contains methods for comparing the minimum descriptors of datasets

import ILP_linear as solver
import os, re

# takes in a descriptor set D and converts it into an array of arrays of integers
def string_descriptor_to_array(D):
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
            descriptors.append(descriptor)

    return descriptors


# find the descriptors of the given data sets
# parameter:
#       - directory: the name of a directory in the perturb_testing folder
def find_descriptors(directory):
    # generate a list of the files to test
    test_files = os.listdir(f"perturb_testing/{directory}/")
    delta_files = os.listdir(f"perturb_testing/{directory}_delta/")
    # create an empty list of solutions
    solutions = []
    # for each data set
    for file in test_files:
        # add each solution to the solutions array
        solutions.append(solver.ILP_linear(f"perturb_testing/{directory}/{file}"))

    # create a empty list of deltas
    deltas_text = ["" for i in range(len(delta_files))]
    # for each delta
    for i, file in enumerate(delta_files):
        # open the file
        with open(f"perturb_testing/{directory}_delta/{file}") as f:
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
                deltas_temp[i] = d.split(", ")
        # append the list of deltas, remove last index because it is always empty
        deltas.append(deltas_temp[:len(deltas_temp)-1])

    # create an empty list of sets of descriptors
    descriptors = []
    # for each descriptor set
    for s in solutions:
        # append the string form of each descriptor set to the list of descriptor sets
        descriptors.append(string_descriptor_to_array(s))

    # for each delta in the set of deltas
    for i, delta in enumerate(deltas):
        # for each number tag pair
        for j, number_tag in enumerate(delta):
            # for each number in the pair
            for k, number in enumerate(number_tag):
                # cast to an integer
                deltas[i][j][k] = int(number)

    # generate a list of the sizes of each descriptor
    descriptor_sizes = [[len(descriptors[i][j]) for j in range(len(descriptors[i]))] for i in range(len(descriptors))]

    # copy descriptor_sizes one list at a time
    change_size = [descriptor_sizes[i].copy() for i in range(len(descriptor_sizes))]
    # for each descriptor set
    for i, descriptor_set in enumerate(descriptor_sizes):
        # for each size in the descriptor set
        for j, size in enumerate(descriptor_set):
            # the change in size is equal to the size minus
            # its corresponding element in the first row of the list
            change_size[i][j] = change_size[i][j] - descriptor_sizes[0][j]

    # copy the descriptors list and call it diff
    # this is done in this manner because it copies the memory address of the internal lists we use descriptors.copy()
    diff = [[descriptors[i][j].copy() for j in range(len(descriptors[i]))] for i in range(len(descriptors))]
    # for each descriptor set in the set of descriptor sets
    for i, descriptor_set in enumerate(descriptors):
        # for descriptor in the descriptor set
        for j, descriptor in enumerate(descriptor_set):
            # for each tag in the descriptor
            for k, tag in enumerate(descriptor):
                # cast to an int
                descriptors[i][j][k] = int(tag)
                # set the value in the diff array to the difference between the two tags
                diff[i][j][k] = descriptors[0][j][k] - descriptors[i][j][k]

    # for each descriptor set
    for i, descriptor_set in enumerate(change_size):
        # skip the first descriptor set because it will not be different from itself
        if i != 0:
            print("-------------------\nAddition(s) to the dataset:")
            # print which tags were added to the dataset
            for j, pair in enumerate(deltas[i-1]):
                print(f"Tag {pair[1]} added to item {pair[0]}")
            print("Cluster changes:")
            # print the changes in the cluster
            for j, change in enumerate(descriptor_set):
                if change > 0:
                    print(f"Some error is causing cluster {j} of dataset {i} to grow larger")
                elif change < 0:
                    print(f"Cluster {j} of the dataset {i} shrinks by {size}")


find_descriptors("4x14")
