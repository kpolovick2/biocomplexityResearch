"""answer_to_data.py: generates synthetic data sets that always have solutions"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

import random
import math


def sample_with_exclusion(lower, upper, exclude, n):
    """
    generate a random number from a set of numbers while excluding a set of numbers
    :param lower: the lower bound of the range
    :param upper: the upper bound of the range
    :param exclude: a list of numbers to be excluded from the sampling
    :param n: the number of numbers to be returned (sampled)
    :return: a list of n numbers within the specified range that are not contained within the exclude list
    """
    # generate a random sample, but exclude the excluded values
    s = set(range(lower, upper)) - set(exclude)
    # cast back to a list and return
    return random.sample(list(s), n)


def generate(n, K, N, alpha, beta, min_alpha, min_tags, max_tags, min_items, max_items, percent_overlap):
    """
    a function that generates a minimum descriptor
    :param n: n
    :param K: K
    :param N: N
    :param alpha: alpha
    :param beta: beta
    :param min_alpha: the smallest size of any descriptor in the dataset (size permitting)
    :param min_tags: the minimum number of tags an item can have
    :param max_tags: the maximum number of tags an item can have
    :param min_items: the minimum number of items a cluster can have
    :param max_items: the maximum number of items a cluster can have
    :param percent_overlap: the percentage of items outside the descriptor that overlap within a cluster
    :return: void, outputs a synthetic dataset
    """
    # generate a synthetic descriptor set
    D = generate_descriptors(K, N, alpha, beta, min_alpha)

    # make an empty B matrix
    B = [[0 for i in range(N)] for j in range(n)]
    clusters = []

    # calculate K / n to ensure roughly even assignment of cluster values
    n_over_k = math.floor(n / K)
    # make a variance value that affects the number of items that are assigned to each cluster
    variance = 0
    # if n >= 10, make variance the floor of n/10
    if n >= 10:
        variance = math.floor(n / 10)

    # for each cluster, assign a number of items between
    # n/K - variance and n/K + variance (inclusive)
    # with the designated k value
    for i in range(K):
        # generate a number of items to add to the cluster. ensure that this value is between the max_tags value
        items_in_cluster = random.choice(range(max(n_over_k - variance, min_items),
                                               min(n_over_k + variance + 1, max_items)))

        # if adding this number of items to the cluster would prevent every
        # cluster from having an item, set items_in_cluster to 1
        if (K - len(clusters) - items_in_cluster) / (K - i) < 1:
            items_in_cluster = 1
        # fill the clusters array
        for j in range(items_in_cluster):
            clusters.append(i + 1)

    # make a list of tags that cannot be used to ensure that there is a solution
    unusable_tags = []
    for desc in D:
        for i in desc:
            unusable_tags.append(i - 1)

    # fill the unfilled clusters indices with the largest cluster value
    while len(clusters) < n:
        clusters.append(K)

    # for every item
    for i in range(n):
        # get the k value of the item
        k = clusters[i]

        # assign a random tag from the corresponding descriptor equal to 1
        B[i][random.choice(D[k - 1]) - 1] = 1

    # create a list of unusable tags within a given cluster
    unusable_tags_within_k = [unusable_tags for i in range(K)]
    # previous_tags = []
    # iterate over the set of data items and assign tags
    for i in range(len(B)):
        row = B[i]
        k = clusters[i]

        # generate a number of tags for the data item to have
        num_tags = random.choice(range(min_tags - 1, max_tags))
        # generate the tags to add by selecting from a range of tag values
        # and excluding the tags that are used in the descriptor
        num_tags = min(num_tags, N - len(unusable_tags))
        # check bounds
        if num_tags > 0:
            # take a random sample of tags to include
            tags_to_add = sample_with_exclusion(0, N, unusable_tags_within_k[k-1], num_tags)
            # update the unusable tags within this cluster if the random number is above the percent_overlap
            if random.choice(range(100)) > percent_overlap:
                unusable_tags_within_k[k-1] = list(set(unusable_tags_within_k[k-1]) - set(tags_to_add))
            # set the tags values to 1
            for tag in tags_to_add:
                row[tag] = 1
            # previous_tags = tags_to_add

    # commented print statements
    # for i in range(n):
    #     print(f"k={clusters[i]} : {B[i]}")

    # set the first line of the output file to the following
    output_text = f"{n} {K} {N} {alpha} {beta} \n"
    # generate a file name
    file_name = f"{n}n_{K}K_{N}N_{alpha}a_{beta}b"
    # append each line of the B matrix to the string
    for i in range(len(B)):
        # prepend the item and cluster numbers
        output_text += f"{i + 1} {clusters[i]} "
        for j in range(len(B[i])):
            # add each B value
            output_text += f"{B[i][j]} "
        # add a new line character
        output_text += "\n"

    # generate the output file
    with open(f"../test_txt_files/{file_name}.txt", 'w') as f:
        f.write(output_text)

    return output_text


def remove_tags(usable_tags, used_tags):
    """
    removes tags from a set of usable tags
    :param usable_tags: a list of tags
    :param used_tags: a list of unwanted tags
    :return: the list of tags with the list of unwanted tags removed
    """
    # cast the lists to sets, then subtract them
    s = set(usable_tags) - set(used_tags)
    # return the list of the resulting set
    return list(s)


def generate_descriptors(K, N, alpha, beta, min_alpha=1):
    """
    a function that generates a set of descriptors given K, N, alpha, and beta
    :param K: K
    :param N: N
    :param alpha: alpha
    :param beta: beta
    :param min_alpha: the smallest size of any descriptor (size permitting)
    :return: list D (a set of descriptors)
    """
    # create an empty set of descriptors
    D = [[] for i in range(K)]

    # make a list containing every tag
    usable_tags = list(range(1, N + 1))

    # generate descriptors
    for i in range(len(D)):
        # generate a number of tags for the selected descriptor
        num_tags = random.choice(range(min_alpha, alpha + 1))

        # check to make sure that the remaining number of tags
        # can still be assigned to a cluster with the given alpha value
        if (len(usable_tags) - num_tags) / (K - i) < 1:
            num_tags = 1
        # set the current descriptor to be a random sample of the usable tags
        descriptor = random.sample(usable_tags, min(num_tags, len(usable_tags)))

        # remove the tags used in this descriptor
        usable_tags = remove_tags(usable_tags, descriptor)
        # assign the index of D to the descriptor
        D[i] = descriptor

    # create an array to store if a tag in a descriptor has been updated
    already_overlapping = [[False for i in range(len(D[j]))] for j in range(len(D))]

    # correct to ensure beta overlap
    for b in range(beta):
        # choose a random descriptor
        x = random.choice(range(len(D)))
        # choose a random tag from that descriptor
        y = random.choice(range(len(D[x])))
        # set the overlapping tag value to be the chosen tag from the chosen descriptor
        overlapping_tag = D[x][y]
        # make a temp variable to store if a change has been made
        change_made = False

        # while no change has been made
        while not change_made:
            # choose a random descriptor
            xx = random.choice(range(len(D)))
            # choose a random tag from that descriptor
            yy = random.choice(range(len(D[xx])))

            # if the overlapping tag is not equal to the selected tag,
            #       they are not from the same descriptor,
            #       and the tag has not already been updated
            if not overlapping_tag == D[xx][yy] and x != xx and not already_overlapping[xx][yy]:
                # change the tag to be equal to the overlap tag
                D[xx][yy] = overlapping_tag
                # store that this tag was updated
                already_overlapping[xx][yy] = True
                # change temp variable to exit the loop
                change_made = True
    print(D)
    return D


generate(n=1000, K=6, N=40, alpha=4, beta=1, min_alpha=4, min_tags=4, max_tags=9, min_items=120,
         max_items=180, percent_overlap=15)
