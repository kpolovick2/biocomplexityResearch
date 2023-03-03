# Name: Keara Polovick (and William Bradford)
# Computing ID: uzy2ws (and wcb8ze)
# duplicate of ILP_gurobi for the purpose of generalizing the algorithm
# has a faster runtime complexity than the standard generalized version

# changes: make gurobi output in order of k value instead of j

from gurobipy import LinExpr, QuadExpr

import gurobipy as gp


def dot(arr1, arr2):
    answer = 0
    for i in range(len(arr1)):
        answer += (arr1[i] * arr2[i])
    return answer


def add(arr1, arr2):
    answer = []
    for i in range(len(arr1)):
        answer.append(arr1[i] + arr2[i])
    return answer


def ILP_linear(filename):

    with open(filename) as f:
        input = f.read()

    input.replace("\n", "")
    input_array = input.split()
    n = int(input_array[0])  # number of data items
    K = int(input_array[1])  # number of clusters
    N = int(input_array[2])  # number of tags
    alpha = int(input_array[3])  # maximum size of descriptor for each item
    beta = int(input_array[4])  # maximum overlap

    B = []
    clusters = []
    for i in range(n):
        B.append([])
        clusters.append(int(input_array[i * (N + 2) + 6]))
        for j in range(N):
            B[i].append(int(input_array[i*(N+2)+7+j]))


    m = gp.Model()

    #create y[j,k] variables
    y= {}
    for j in range(1, N+1):
        for k in range(1, K+1):
            y[j,k] = m.addVar(vtype='B', name="k=%s y[%s,%s]"%(k,j,k))
    m.update()

    # Objective function is to minimize the sum of the variables in A
    coef = [1 for j in range(1, N+1) for k in range(1,K+1)]
    var = [y[j, k] for j in range(1, N+1) for k in range(1,K+1)]
    objective = m.setObjective(LinExpr(coef, var), gp.GRB.MINIMIZE)
    m.update()

    # CONSTRAINTS

    # print("Constraint A: ")
    #(a) must contain at least one tag from each of the data items in that cluster --ALL GOOD
    A = [0 for c in range(n+1)]
    constraint1 = []
    for i in range(1,n+1):
        for j in range(1,N+1):
            k = clusters[i-1]
            if B[i - 1][j - 1] == 1:
                A[i] += y[j, k]
        constraint1.append(m.addConstr(A[i], ">=", 1))
        m.update()
    #     print(f"{m.getRow(constraint1[i - 1])} {constraint1[i - 1].Sense} {constraint1[i - 1].RHS}")
    #
    # print("------------------------")

    # print("Constraint B: ")
    #(b) size of each descriptor must be at most alpha --ALL GOOD
    columns = []                                # set up the columns array for later use in part C
    coef = [1 for j in range(1, N + 1)]
    for k in range(1, K+1):
        var = [y[j, k] for j in range(1, N+1)]
        columns.append(var)
        constraint2 = m.addConstr(LinExpr(coef, var), "<=", alpha)
        m.update()
        # print(f"{m.getRow(constraint2)} {constraint2.Sense} {constraint2.RHS}")

    # print("------------------------")
    #
    # print("Constraint C: ")

    # (c) overlap between any pair of descriptors must be at most beta --ALL GOOD
    # this version of the algorithm uses vector operations (dot product and add)
    # to build constraint c asymptotically faster than the alternative

    z = {}
    z_sum = 0
    for k in range(1, K):
        for l in range(k + 1, K + 1):
            for j in range(1, N + 1):
                if B[k-1][j-1] * B [l-1][j-1] == 1:
                    z[j, k, l] = m.addVar(vtype='B', name=f"z[%s,%s,%s]" % (j, k, l))
                    m.addConstr(z[j,k,l], "<=", y[j, k])
                    m.addConstr(z[j,k,l], "<=", y[j, l])
                    m.addConstr(z[j,k,l], ">=", y[j,k] + y[j,l] - 1)
                    z_sum += z[j,k,l]
                    m.update()
    constraint3 = m.addConstr(z_sum, gp.GRB.LESS_EQUAL, beta)
    m.update()

    # z_sum_2 = 0
    # internal_sum = columns[K-1]
    # for k in range(K-1, 0, -1):
    #     z_sum_2 += dot(columns[k-1], internal_sum)
    #     internal_sum = add(columns[k-1], internal_sum)
    #
    # constraint3 = m.addConstr(z_sum_2, gp.GRB.LESS_EQUAL, beta)
    # m.Params.PreQLinearize = 2
    # m.update()
    # print(f"{m.getQCRow(constraint3)} {constraint3.QCSense} {constraint3.QCRHS}")
    # print("------------------------")


    m.optimize()

    # get the values of variables
    x_values = m.getAttr("X")
    y_values = m.getVars()

    # make an array of the names of used variables
    vars_used = []
    for i in range(len(x_values)):
        if x_values[i] == 1.0:
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
    # return m.getAttr("X")

    print(output_string)
    return output_string

# ILP_linear("test_txt_files/example_2.txt")