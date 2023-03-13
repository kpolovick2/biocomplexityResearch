# Name: Keara Polovick
# Computing ID: uzy2ws

from gurobipy import LinExpr

import gurobipy as gp
m = gp.Model()

n= 4    #total number of data items
N= 4    #total number of tags
K= 2    #number of clusters
alpha= 2
beta= 1

B= [[1,1,0,0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]

#create y[j,k] variables
y= {}
for j in range(1, N):
    for k in range(1, K):
        y[j,k] = m.addVar(vtype='B', name="y[%s,%s]"%(j,k))

m.update()

#create A value to be minimized (can't be a var)
A = 0
for j in range(1, N):
    for k in range(1, K):
        A += y[j,k]

#Objective function is to minimize the sum of the variables in A
m.setObjective(A, gp.GRB.MINIMIZE)


#CONSTRAINTS

#(a) must contain at least one tag from each of the data items in that cluster
for i in range(1, n):
    A1= 0
    for j in range(1, N):
        for k in range(1, K):
            if B[i][j]==1:
                A1 += y[j,k]
    #Constraint: sum of variables in A should be >= 1
    m.addConstr(A1, ">=", 1)

#(b) size of each descriptor must be at most alpha
for k in range(1, K):
    coef = [1 for j in range(1, N)]
    var = [y[j, k] for j in range(1, N)]
    m.addConstr(LinExpr(coef, var), "<=", alpha)

#(c) overlap between any pair of descriptors must be at most beta
z= {}
for j in range(N):
    for k in range(K-1):
        for l in range(k+1, K-1):   #had to change to K-1 because of key error
            z[j,k,l]= y[j,k]*y[j,l]

coef= [1 for j in range(N)]
for k in range(1, K-1):
    for l in range(k+1, K):
        var= [z[j,k,l] for j in range(N)]
        m.addConstr(LinExpr(coef, var), "<=", beta)


m.optimize()

print(f"Optimal objective value: {m.objVal}")

print(f"Solution values: A= {A}, y[1,1]= {y[1,1]}, y[2,1]= {y[2,1]}, y[3,1]= {y[3,1]}")

