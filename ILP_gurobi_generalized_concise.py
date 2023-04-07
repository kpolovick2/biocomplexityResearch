# Name: Keara Polovick (and William Bradford)
# Computing ID: uzy2ws (and wcb8ze)
# duplicate of ILP_gurobi for the purpose of generalizing the algorithm
# has a faster runtime complexity than the standard generalized version

# changes: make gurobi output in order of k value instead of j

from gurobipy import LinExpr, QuadExpr

import gurobipy as gp

# helper function that takes the dot product of two arrays
def dot(arr1, arr2):
    answer = 0
    for i in range(len(arr1)):
        answer += (arr1[i] * arr2[i])
    return answer

# helper function that adds the ith elements of two arrays,
# then stores the resulting value in another array's ith index
def add(arr1, arr2):
    answer = []
    for i in range(len(arr1)):
        answer.append(arr1[i] + arr2[i])
    return answer

# takes a file as an argument and finds the minimum descriptor of the file using integer quadratic programming
def ILP_concise(filename):


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
    K_VALUE_OFFSET = 6   # the six is the offset that describes the location of each K value within the array
    FIRST_TAG_INDEX = 7  # the seven corresponds to the location of the first tag value in the input array
    B = []
    clusters = []
    for i in range(n):
        # create an empty line in B
        B.append([])
        clusters.append(int(input_array[i * (N + 2) + K_VALUE_OFFSET]))
        for j in range(N):
            B[i].append(int(input_array[i*(N+2)+ FIRST_TAG_INDEX +j]))
    m = gp.Model()

    #create y[j,k] variables
    y = {}
    for j in range(1, N+1):
        for k in range(1, K+1):
            y[j,k] = m.addVar(vtype='B', name="k=%s y[%s,%s]"%(k,j,k))
    m.update()

    # Objective function is to minimize the sum of the y[j,k] variables
    coef = [1 for j in range(1, N+1) for k in range(1,K+1)]
    var = [y[j, k] for j in range(1, N+1) for k in range(1,K+1)]
    m.setObjective(LinExpr(coef, var), gp.GRB.MINIMIZE)
    m.update()

    # CONSTRAINTS

    #(a) must contain at least one tag from each of the data items in that cluster
    A = [0 for c in range(n+1)]
    constraint1 = []
    for i in range(1,n+1):
        for j in range(1,N+1):
            k = clusters[i-1]
            if B[i - 1][j - 1] == 1:
                A[i] += y[j, k]
        constraint1.append(m.addConstr(A[i], ">=", 1))
        m.update()

    #(b) size of each descriptor must be at most alpha
    columns = []                                # set up the columns array for later use in part C
    coef = [1 for j in range(1, N + 1)]
    for k in range(1, K+1):
        var = [y[j, k] for j in range(1, N+1)]
        columns.append(var)
        m.addConstr(LinExpr(coef, var), "<=", alpha)
        m.update()

    # (c) overlap between any pair of descriptors must be at most beta
    # this version of the algorithm uses vector operations (dot product and add)
    # to build constraint c asymptotically faster than the alternative
    z_sum_2 = 0
    internal_sum = columns[K-1]
    for k in range(K-1, 0, -1):
        z_sum_2 += dot(columns[k-1], internal_sum)
        internal_sum = add(columns[k-1], internal_sum)

    m.addConstr(z_sum_2, "<=", beta)
    m.update()

    m.optimize()

    # get the values of variables
    x_values = m.getAttr("X")
    y_values = m.getVars()

    # make an array of the names of used variables
    vars_used = []
    for i in range(len(x_values)):
        if x_values[i] == 1.0:
            # adds a string containing the name of the variable
            vars_used.append(y_values[i].getAttr("VarName"))

    # sort the array alphabetically
    vars_used.sort()

    output_string = ""
    # print the values of the solution that equal one
    print("Solution:\n---------------------------")
    for var in vars_used:
        # use a temp variable to only output the variable's name rather than the k value
        temp = var.split()
        output_string += f"{temp[1]} = 1\n"

    print(output_string)
    return output_string

#ILP_concise("test_txt_files/[UCI] AAAI-14 Accepted Papers - Papers.csv");

ILP_concise("test_txt_files/4x14.txt")
print("----------------------------------")
print("ADDITION OF TAGS: 10 data items, 4 clusters (pertubed so that all tags describe data item 1)")
print("----------------------------------")
ILP_concise("test_txt_files/4x14_pertubed.txt")

print("----------------------------------")
print("DELETION OF TAGS: 10 data items, 4 clusters (delete 1 tags from data item 1)")
print("----------------------------------")
ILP_concise("test_txt_files/4x14_deletion_of_tags.txt")