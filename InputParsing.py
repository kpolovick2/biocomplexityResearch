# William Braford
# wcb8ze
# 2/17/2023

def get_B_matrix(input):
    input.replace("\n", "")
    input_array = input.split()
    n = int(input_array[0])  # number of data items
    K = int(input_array[1])  # number of clusters
    N = int(input_array[2])  # number of tags
    alpha = int(input_array[3])  # maximum size of descriptor for each item
    beta = int(input_array[4])  # maximum overlap

    B = []
    for i in range(n):
        temp = []
        for j in range(N):
            temp.append(int(input_array[i*(N+2)+7+j]))
        B.append(temp)

    clusters = []
    for i in range(n):
        clusters.append(int(input_array[i*(N+2)+6]))

    print(B)
    print(clusters)

with open('input.txt') as f:
    exin = f.read()

get_B_matrix(exin)
