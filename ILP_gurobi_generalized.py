# Name: Keara Polovick (and William Bradford)
# Computing ID: uzy2ws (and wcb8ze)
# duplicate of ILP_gurobi for the purpose of generalizing the algorithm

from gurobipy import LinExpr, QuadExpr

import gurobipy as gp
import time

start = time.time()

with open('input.txt') as f:
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
    temp = []
    clusters.append(int(input_array[i * (N + 2) + 6]))
    for j in range(N):
        temp.append(int(input_array[i*(N+2)+7+j]))
    B.append(temp)


m = gp.Model()

#create y[j,k] variables
y= {}
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
A = [0 for c in range(n+1)]
constraint1 = []
for i in range(1,n+1):
    for j in range(1,N+1):
        k = clusters[i-1]
        if B[i - 1][j - 1] == 1:
            A[i] += y[j, k]
    constraint1.append(m.addConstr(A[i], ">=", 1))
    m.update()
    print(f"{m.getRow(constraint1[i - 1])} {constraint1[i - 1].Sense} {constraint1[i - 1].RHS}")


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

z_sum = 0
for k in range(1, K):
    for l in range(k+1, K+1):
        for j in range(1, N+1):
            z_sum = gp.quicksum([z_sum, y[j,k]*y[j,l]])


# coef = [1 for k in range(1,K) for l in range(k+1, K+1) for j in range(1, N+1)]
# var= [z[j,k,l] for k in range(1,K) for l in range(k+1, K+1) for j in range(1, N+1)]
# varsum = gp.quicksum(var)

constraint3 = m.addConstr(z_sum, gp.GRB.LESS_EQUAL, beta)
m.update()
print(f"{m.getQCRow(constraint3)} {constraint3.QCSense} {constraint3.QCRHS}")
print("------------------------")


m.optimize()

print("-------------------------------------------\nSolution:")

m.printAttr("X")

#
# print(f"Optimal objective value: {m.objVal}")
#
# print(f"Solution values: A= {A}, y[1,1]= {y[1,1].X}, y[2,1]= {y[2,1].X}, y[3,1]= {y[3,1].X}")


print(f"\nexecution time: {time.time()-start}")