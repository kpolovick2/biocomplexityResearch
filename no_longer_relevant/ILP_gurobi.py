# Name: Keara Polovick (and William Bradford)
# Computing ID: uzy2ws (and wcb8ze)

from gurobipy import LinExpr, QuadExpr

import gurobipy as gp

m = gp.Model()

n= 4    #total number of data items
N= 4    #total number of tags
K= 2    #number of clusters
alpha= 2
beta= 1

B= [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]

#create y[j,k] variables
y= {}
y_int = []
for j in range(1, N+1):
    for k in range(1, K+1):
        y[j,k] = m.addVar(vtype='B', name="y[%s,%s]"%(j,k))
m.update()

#Objective function is to minimize the sum of the variables in A
coef = [1 for j in range(1, N+1) for k in range(1,K+1)]
var = [y[j, k] for j in range(1, N+1) for k in range(1,K+1)]
objective= m.setObjective(LinExpr(coef, var), gp.GRB.MINIMIZE)
m.update()

#CONSTRAINTS

print("Constraint A: ")
#(a) must contain at least one tag from each of the data items in that cluster --FIX
for i in range(1,n+1):
    A1= 0
    for j in range(1,N+1):
        #if data item is in cluster 1, k=1
        #if data item is in cluster 2, k=2
        k=1 # how do you know which cluster the data item is in?
        if B[i-1][j-1]==1:
            A1 += y[j,k]

    #Constraint: sum of variables in A should be >= 1
    constraint1 = m.addConstr(A1, ">=", 1)
    m.update()
    print(f"{m.getRow(constraint1)} {constraint1.Sense} {constraint1.RHS}")

print("------------------------")

print("Constraint B: ")
#(b) size of each descriptor must be at most alpha --ALL GOOD
for k in range(1, K+1):
    coef = [1 for j in range(1, N+1)]
    var = [y[j, k] for j in range(1, N+1)]
    constraint2= m.addConstr(LinExpr(coef, var), "<=", alpha)
    m.update()
    print(f"{m.getRow(constraint2)} {constraint2.Sense} {constraint2.RHS}")

print("------------------------")

print("Constraint C: ")
#(c) overlap between any pair of descriptors must be at most beta --FIX
z = {}
z_sum = 0
for k in range(1, K):
    for l in range(k+1, K+1):
        for j in range(1, N+1):
            z[j,k,l] = y[j,k]*y[j,l]
            z_sum = gp.quicksum([z_sum, z[j,k,l]])


# coef = [1 for k in range(1,K) for l in range(k+1, K+1) for j in range(1, N+1)]
var= [z[j,k,l] for k in range(1,K) for l in range(k+1, K+1) for j in range(1, N+1)]
varsum = gp.quicksum(var)

constraint3 = m.addConstr(varsum, gp.GRB.LESS_EQUAL, beta)
m.update()
print(f"{m.getQCRow(constraint3)} {constraint3.QCSense} {constraint3.QCRHS}")
print("------------------------")


m.optimize()

print(f"Optimal objective value: {m.objVal}")
#
print(f"Solution values: A= {A1}, y[1,1]= {y[1,1].X}, y[2,1]= {y[2,1].X}, y[3,1]= {y[3,1].X}")

