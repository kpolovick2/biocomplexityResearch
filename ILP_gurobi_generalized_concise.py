# Name: Keara Polovick (and William Bradford)
# Computing ID: uzy2ws (and wcb8ze)
# linear version of ILP

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


def form_z(vector, vector_sum):
    if len(vector_sum) == 0:
        return vector
    else:
        return [add(vector, vector_sum), dot(vector, vector_sum)]


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
            y[j,k] = m.addVar(vtype='B', name="y[%s,%s]"%(j,k))
    m.update()

    # Objective function is to minimize the sum of the variables in A
    coef = [1 for j in range(1, N+1) for k in range(1,K+1)]
    var = [y[j, k] for j in range(1, N+1) for k in range(1,K+1)]
    objective = m.setObjective(LinExpr(coef, var), gp.GRB.MINIMIZE)
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
    #     print(f"{m.getRow(constraint1[i - 1])} {constraint1[i - 1].Sense} {constraint1[i - 1].RHS}")


    #(b) size of each descriptor must be at most alpha
    columns = []                                # set up the columns array for later use in part C
    coef = [1 for j in range(1, N + 1)]
    for k in range(1, K+1):
        var = [y[j, k] for j in range(1, N+1)]
        columns.append(var)
        constraint2 = m.addConstr(LinExpr(coef, var), "<=", alpha)
        m.update()
        # print(f"{m.getRow(constraint2)} {constraint2.Sense} {constraint2.RHS}")


    # (c) z[j,k,l]<= y[j,k] and z[j,k,l] ,= y[j,l]
    L= 0.5*K
    z=[]
    for j in range(1, N):
        for k in range(1, L):
            for l in range(L+1,K):
                if(y[j,k]==0 or y[j,l]==0):
                    m.addConstr(z[j,k,l], gp.GRB.LESS_EQUAL, y[j,k])
                    m.addConstr(z[j, k, l], gp.GRB.LESS_EQUAL, y[j, l])
                elif(y[j,k]==1 or y[j,l]==1):
                    m.addConstr(z[j, k, l], gp.GRB.GREATER_EQUAL, y[j,k]+y[j,l]-1)


    # (d) overlap between any pair of descriptors must be at most beta
    z_sum_2 = 0
    internal_sum = columns[K - 1]
    for k in range(K - 1, 0, -1):
        z_sum_2 += dot(columns[k - 1], internal_sum)
        internal_sum = add(columns[k - 1], internal_sum)

    constraint3 = m.addConstr(z_sum_2, gp.GRB.LESS_EQUAL, beta)
    m.update()
    # print(f"{m.getQCRow(constraint3)} {constraint3.QCSense} {constraint3.QCRHS}")

    m.optimize()
    # m.printAttr("X")
    return m.getAttr("X")