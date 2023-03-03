# William Bradford
# wcb8ze
# solution checker file to verify that solutions truly are minimum descriptors for the problem in question

import ILP_linear as ilp

def check(solution_string, filename):

    with open(filename) as f:
        input = f.read()

    input.replace("\n", "")
    input_array = input.split()
    n = int(input_array[0])  # number of data items
    K = int(input_array[1])  # number of clusters
    N = int(input_array[2])  # number of tags
    alpha = int(input_array[3])  # maximum size of descriptor for each item
    beta = int(input_array[4])  # maximum overlap

    # create the list of which data items belong to which clusters
    # create the matrix of tags
    B = []
    clusters = []
    for i in range(n):
        B.append([])
        clusters.append(int(input_array[i * (N + 2) + 6]))
        for j in range(N):
            B[i].append(int(input_array[i*(N+2)+7+j]))

    # initialize array to store tags of the solution
    tags_by_cluster = [[] for i in range(K+1)]

    #split the output into a usable format
    y_strings = solution_string.split("\n")
    for y in y_strings:
        if y != "":
            half = y.split(",")
            tag = half[0].split("[")[1]
            cluster = half[1].split("]")[0]
            tags_by_cluster[int(cluster)].append(int(tag))

    print("--------------------------------\nCheck that each item is covered:\n--------------------------------")
    # verify that each data item is described by a tag found in the solution
    for i in range(len(B)):
        current_k = clusters[i] # query the current cluster
        data_item = B[i] # query the current data item
        tags = tags_by_cluster[current_k] # query the tags associated with the cluster in this solution
        tag_found = False

        # make sure that the current data item i+1 is described by at least one tag from its cluster
        for tag in tags:
            if data_item[tag-1] == 1:
                tag_found = True
                break

        # terminate and return false if item is not covered
        if tag_found == False:
            print(f"Tag not found for data item {i+1} in cluster {current_k}, solution not valid.")
            return False
        else:
            print(f"All tags found for data item {i+1} in cluster {current_k}.")

    print("\nAll data items are covered.\n")

    print("----------------------\nCheck beta constraint:\n----------------------")
    # verify that each tag is used as most beta times
    tag_list = []

    # convert the tags into a list of tags, preserving duplicates
    for tag_set in tags_by_cluster:
        for tag in tag_set:
            tag_list.append(tag)

    for tag in tag_list:
        use_count = 0 # stores the number of times a tag is used

        # compare the current tag to every tag in the tag list
        for alt_tag in tag_list:
            if tag == alt_tag:
                use_count += 1

        # if the tag is used more than beta times, terminate and return false
        if use_count <= beta:
            print(f"Solution does not overuse tag {tag}.")
        else:
            print(f"Solution overuses tag {tag}. It was used {use_count} times across all clusters.")
            return False

    print("\nBeta constraint satisfied.\n")

    print("----------------------\nCheck alpha constraint:\n----------------------")
    # verify that each cluster is described by at most alpha tags
    for i in range(len(tags_by_cluster)):

        # if the size of each cluster's descriptor is greater than alpha, terminate and return false
        if len(tags_by_cluster[i]) > alpha:
            print(f"Cluster {i+1} is described by {len(tags_by_cluster)} tags, which is greater than {alpha}.")
            return False
        else:
            print(f"Cluster {i+1} satisfies the alpha constraint.")

    print("\nAlpha constraint satisfied.\n")

    print("All constraints satisfied.")
    return True

check(ilp.ILP_linear("test_txt_files/100n_7K_100N_15a_1b.txt"), "test_txt_files/100n_7K_100N_15a_1b.txt")