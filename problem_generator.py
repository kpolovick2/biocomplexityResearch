# William Bradford
# wcb8ze
# generation script for minimum descriptor problems

import random
import math

# request: input total number of tags, total number of data items, total number of clusters,
# max tags/data item

# TODO: add max_items

# a function to generate synthetic data from inputs n, K, N, alpha, beta,
# max_tags (the max number of tags per item)
# min_tags (the min number of tags per item)
# min_items (the minimum number of items per cluster, item count permitting)
# percent_overlap (the percentage of overlap between items, ranging from 0 to 100)
#            this means that, in the set, this percentage or more of items will
#            have at least one overlapping tag
def generate(n, K, N, alpha, beta, max_tags, min_tags, min_items, percent_overlap):
    # assigns the first line of the output file
    output_s = f"{n} {K} {N} {alpha} {beta}\n"
    # auto-generate the file name
    filename = f"{n}n_{K}K_{N}N_{alpha}a_{beta}b"
    # generate a list of chance values for the overlapping items
    overlapping_items = random.choices(range(0, 100), k=n)

    overlap_count = 0
    # count the number of overlapping items
    for i in range(n):
        if overlapping_items[i] < percent_overlap:
            overlap_count += 1

    # if the number of overlaps is less than the desired amount
    if overlap_count/n < percent_overlap/100:
        # store the number of items that need to be 'fixed'
        fix_count = math.floor((percent_overlap*n/100)) - overlap_count
        while fix_count > 0:
            # generate a random index
            index = random.randint(0, n-1)
            change = False
            # while no item has been changed
            while not change:
                # if the item is not going to overlap, correct it to overlap
                if overlapping_items[index] > percent_overlap:
                        overlapping_items[index] = 0
                        fix_count -= 1
                        change = True
                # if there is a collision, increment the index to be changed
                else:
                    index += 1

    k_used = {} # used to store which clusters have items in them
    previous_tags = random.sample(range(0, N-1),
                                  random.randint(min_tags, max_tags)) # used to set up overlap between data items
    for i in range(n):
        # insures that every cluster has at least one data item in it
        if len(k_used) < K:
            k_val = random.randint(1, K)
            while k_val in k_used:
                k_val = k_val % K + 1
        # handles continued addition to the clusters after each cluster has at least one data item in it
        else:
            # print(k_used)
            below_keys = list(dict((key,val) for key, val in k_used.items() if val <= min_items).keys())
            if len(below_keys) != 0:
                k_val = below_keys[random.sample(range(len(below_keys)), 1)[0]]
            # print("---")

        # counts the usages of each k value
        if k_val not in k_used:
            k_used[k_val] = 1
        else:
            k_used[k_val] += 1
        temp_s = f"{i + 1} {k_val} "

        # generate a list of tags that will be used for the current data item
        used_tags = random.sample(range(0, N-1),
                                  random.randint(min_tags, max_tags))
        overlap = 0

        for tag in used_tags:
            if tag in previous_tags:
                overlap += 1

        # correct output to make overlap occur the specified amount of the time or more
        if overlap == 0 and (overlapping_items[i] < percent_overlap):
            used_tags[random.randint(0, len(used_tags)-1)] \
                = previous_tags[random.randint(0, len(previous_tags)-1)]

        # assign the tags to the temp string
        for j in range(N):
            if j in used_tags:
                temp_s += "1 "
            else:
                temp_s += "0 "

        previous_tags = used_tags

        # add new line and move on to the next data item
        temp_s += "\n"
        output_s += temp_s

    # store the synthetic data in a file in the test files folder
    with open(f"test_txt_files/{filename}.txt", 'w') as f:
        f.write(output_s)

# a function that generates a synthetic data set from an input of the number of data items
def parameter_crunch(n):
    K = random.randint(2, n)
    N = random.randint(n, 10 * n)
    alpha = random.randint(2, int(N / 10))
    beta = 1
    generate(n, K, N, alpha, beta)


# n, K, N, alpha, beta, max_tags, min_tags, min_items, percent_overlap
generate(250, 7, 250, 80, 1, 16, 3, 6, 5)
