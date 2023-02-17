# William Braford
# wcb8ze
# 2/17/2023

def parseInput(input):
    input_array = input.split()
    n = int(input_array[0])  # number of data items
    K = int(input_array[1])  # number of clusters
    N = int(input_array[2])  # number of tags
    alpha = int(input_array[3])  # maximum size of descriptor for each item
    beta = int(input_array[4])  # maximum overlap

    B = []
    for i in range(n):
        if int(input_array[i*(N+2)+6]) == 1 or 1==1:
            temp = []
            for j in range(N):
                temp.append(int(input_array[i*(N+2)+7+j]))
            B.append(temp)

    cluster_matrix = []
    for i in range(n):
        cluster_matrix.append(input_array[i*(N+2)+6])

    print(B)
    print(cluster_matrix)

example_input="5 2 7 2 1 " \
              "1 1 1 1 1 0 0 0 0 " \
              "2 1 0 0 0 1 0 0 1 " \
              "3 1 1 0 0 0 1 1 0 " \
              "4 2 0 1 0 1 0 0 1 " \
              "5 2 0 0 0 0 1 1 0 "

parseInput(example_input)
