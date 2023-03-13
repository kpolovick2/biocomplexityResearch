# Name: Keara Polovick
# Computing ID: uzy2ws

from gurobipy import LinExpr, Model

import gurobipy as gp
model = gp.Model()

y= {} #create y-matrix
#y(j,k)

B= {} #create B-matrix

def ilp(N, n, K, k, alpha, beta):
    model = Model("k-median")
    A = {}

    for j in range(1, N):
        for k in range(1, K):
            A += model.addVar(obj= y[j,k], vtype="B", name= "y[%s,%s]"%(j,k))
            model.update()
    #Objective function: is to minimize the sum of the variables in A
    model.setObjective(A, gp.GRB.MINIMIZE)

    #(a) must contain at least one tag from each of the data items in that cluster
    for i in range(1, n):
        A= {}
        for j in range(1, N):
            if B[i,j]==1:
                A += model.addVar(obj= y[j,k], vtype="B", name= "y[%s,%s]"%(j,k))
                model.update()
        #Constraint: sum of variables in A should be >= 1
        model.addConstr(A, ">=", 1)

    #(b) size of each descriptor must be at most a
    for k in range (1, K):
        A= {}
        for j in range (1, N):
            A += model.addVar(obj= y[j,k], vtype="B", name= "y[%s,%s]"%(j,k))
            model.update()
        #Constraint: sum of variables in A should be <= alpha
        model.addConstr(A, "<=", alpha)

    #(c) overlap between any pair of descriptors must be at most B
    for k in range(1, K-1):
        for l in range(k+1, K):
            A= {}
            for j in range(1, N):
                A += model.addVar(obj=y[j, k]*y[j,l], vtype="B", name="y[%s,%s]" % (j, k))
                model.update()
            #Constraint: A should be <= beta
            model.addConstr(A, "<=", beta)


    model.update()
    # model.__data = x,y
    return model

# ilp(4, 5, 2, 3, 2, 1)
# print("Optimal value=", model.ObjVal)