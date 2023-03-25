# William Bradford
# wcb8ze
# generation script for minimum descriptor problems

import random
import math


# generate a random number from a set of numbers while excluding a set of numbers
def sample_with_exclusion(lower, upper, exclude, n):
    # generate a random sample, but exclude the excluded values
    s = set(range(lower, upper)) - set(exclude)
    # cast back to a list and return
    return random.sample(list(s), n)


# generate a synthetic data set from its worst-case descriptors
def generate(n, K, N, alpha, beta, min_tags, max_tags, min_items, max_items):
    # generate a synthetic descriptor set
    D = generate_descriptors(K, N, alpha, beta)

    # make an empty B matrix
    B = [[0 for i in range(n)] for j in range(N)]
    clusters = []

    # calculate K / n to ensure roughly even assignment of cluster values
    n_over_K = math.floor(n / K)
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
        for j in range(random.choice(range(max(n_over_K - variance, min_items),
                                           min(n_over_K + variance + 1, max_items)))):
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
        # assign a random tag from the descriptor equal to 1
        B[i][random.choice(D[k - 1]) - 1] = 1

    # iterate over the set of data items and assign tags
    for row in B:
        # generate a number of tags for the data item to have
        num_tags = random.choice(range(min_tags - 1, max_tags))
        # generate the tags to add by selecting from a range of tag values
        # and excluding the tags that are used in the descriptor
        num_tags = min(num_tags, N - len(unusable_tags))
        # check bounds
        if num_tags > 0:
            # take a random sample of tags to include
            tags_to_add = sample_with_exclusion(0, N, unusable_tags, num_tags)
            # set the tags values to 1
            for tag in tags_to_add:
                row[tag] = 1

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
        output_text += f"{i+1} {clusters[i]} "
        for j in range(len(B[i])):
            # add each B value
            output_text += f"{B[i][j]} "
        # add a new line character
        output_text += "\n"

    # generate the output file
    with open(f"test_txt_files/{file_name}.txt", 'w') as f:
        f.write(output_text)

    return output_text


def remove_tags(usable_tags, used_tags):
    # cast the lists to sets, then subtract them
    s = set(usable_tags) - set(used_tags)
    # return the list of the resulting set
    return list(s)

def generate_descriptors(K, N, alpha, beta):
    D = [[] for i in range(K)]

    usable_tags = list(range(1, N+1))
    use_count = [beta for i in range(N)]

    tags_used = []

    # generate descriptors
    for i in range(len(D)):
        # generate a number of tags for the selected descriptor
        num_tags = random.choice(range(1, alpha+1))
        # set the current descriptor to be a random sample of the usable tags
        descriptor = random.sample(usable_tags, min(num_tags, len(usable_tags)))

        # remove the tags used in this descriptor
        usable_tags = remove_tags(usable_tags, descriptor)
        # assign the index of D to the descriptor
        D[i] = descriptor
        for tag in descriptor:
            tags_used.append(tag)

    already_overlapping = [[False for i in range(len(D[j]))] for j in range(len(D))]

    # correct to ensure beta overlap
    for b in range(beta):
        x = random.choice(range(len(D)))
        y = random.choice(range(len(D[x])))
        overlapping_tag = D[x][y]
        change_made = False
        while not change_made:
            xx = random.choice(range(len(D)))
            yy = random.choice(range(len(D[xx])))
            if not overlapping_tag == D[xx][yy] and x != xx and not already_overlapping[xx][yy]:
                D[xx][yy] = overlapping_tag
                already_overlapping[xx][yy] = True
                change_made = True
    return D


# D, n, K, N, min_tags, max_tags
print(generate(n=10, K=3, N=10, alpha=4, beta=1, min_tags=1, max_tags=5, min_items=2, max_items=5))