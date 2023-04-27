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


def generate(n, K, N, alpha, beta, min_alpha, min_tags, max_tags, min_items, max_items):
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

    # for each cluster, assign a number of items between
    # n/K - variance and n/K + variance (inclusive)
    # with the designated k value
    total_items = 0
    for i in range(K):
        # generate a number of items to add to the cluster. ensure that this value is between the max_tags value
        items_in_cluster = random.choice(range(min_items,
                                               max_items))
        total_items += items_in_cluster
        # if adding this number of items to the cluster would prevent every
        # cluster from having an item, set items_in_cluster to 1
        # if (n - total_items) / (K - i) < 1:
        #     items_in_cluster = 1
        # fill the clusters array
        for j in range(items_in_cluster):
            clusters.append(i + 1)

    # make a list of tags that cannot be used to ensure that there is a solution
    unusable_tags_within_k = []
    for desc in D:
        # this list will be empty for each cluster to begin with
        unusable_tags_within_k.append([])

    # fill the unfilled clusters indices with the largest cluster value
    while len(clusters) < n:
        clusters.append(K)

    # a list that will store the number of appearances of each descriptor tag within the set
    tag_appearances = [[0 for j in range(len(D[i]))] for i in range(len(D))]
    # an list that will store the indices of the tag that describes item i at position (re-indexing at 0)
    describing_tag = [0 for i in range(n)]

    # for every item
    for i in range(n):
        # get the k value of the item
        k = clusters[i]
        # find the tag that will describe item i
        tag = random.choice(D[k - 1]) - 1
        # store the index within the descriptors array at position k-1
        descriptor_index = D[k-1].index(tag+1)
        # assign a random tag from the corresponding descriptor equal to 1
        B[i][tag] = 1
        # store the tag that describes item i in position i (re-indexing at 0)
        describing_tag[i] = descriptor_index
        # increment the number corresponding to the amount of appearances of each tag within the descriptor
        tag_appearances[k-1][descriptor_index] += 1
        # print(f"{i} : {B[i]}")

    # generate a list of the tags used by all the items that correspond to each describing tag in each cluster
    tag_usage_by_cluster = [[[0 for n in range(N)] for j in range(len(D[k]))] for k in range(len(D))]

    # iterate over the set of data items and assign tags
    for i in range(len(B)):
        # row is the row of tags corresponding to item i (re-indexing at 0)
        row = B[i]
        # k is the cluster of item i (re-indexing at 0)
        k = clusters[i]
        # d_tag is the tag within the descriptor of cluster k
        # that describes item i (re-indexing at 0)
        d_tag = describing_tag[i]

        # generate a number of tags for the data item to have
        num_tags = random.choice(range(min_tags - 1, max_tags - 1))
        # generate the tags to add by selecting from a range of tag values
        # and excluding the tags that are used in the descriptor,
        # along with the tags that are no longer usable because they would change the solution of the problem
        num_tags = min(num_tags, N - len(unusable_tags_within_k[k - 1]))
        # check bounds
        if num_tags > 0 and len(unusable_tags_within_k[k - 1]) < N:
            # take a random sample of tags to include, exclude all tags that are descriptor tags for the cluster
            # of the current item, and exclude all tags that would change the descriptor if added
            tags_to_add = sample_with_exclusion(0, N, unusable_tags_within_k[k - 1], num_tags)
            # add one to the value corresponding to each tag added in the
            # list of tags used by items within the cluster that are described
            # by d_tag
            for t in tags_to_add:
                tag_usage_by_cluster[k - 1][d_tag][t] += 1

            # make a list to store unusable tags
            becoming_unusable = []
            # each item will be referred to as a d_tag item, meaning the tag that
            # describes it is d_tag within its corresponding descriptor
            # we want each d_tag item to have at most num_appearances(d_tag) - 1
            # appearances within the set of items described by d_tag
            # this ensures that adding it to the descriptor can only increase the size
            # of the descriptor, making it no longer a minimum descriptor
            # to begin, we iterate over the list that contains usage counts for each tag
            # in the set of d_tag items
            for i, use_count in enumerate(tag_usage_by_cluster[k - 1][d_tag]):
                # if the number of appearances of d_tag is less than or equal to
                # the number of usages of the tag i,...
                if tag_appearances[k-1][d_tag] <= use_count:
                    # append the tag to the list of unusable tags
                    becoming_unusable.append(i)
            # update the list of unusable tags within the cluster
            unusable_tags_within_k[k - 1] = list(set(unusable_tags_within_k[k - 1]).union(set(becoming_unusable)))
            # add the tags to the items
            for tag in tags_to_add:
                row[tag] = 1

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
    return D
