# Name: Keara Polovick
# Computing ID: uzy2ws


#USING VALUES FROM MATH PROGRAM. DOCUMENT -- EXAMPLE 4
#alpha = 2
#beta = 1
print("-------------------")
print("Example 4 - Math Programming Doc")
print("-------------------")
x1= 5
x2= 6
x3= 7
x4= 8
t1= 1
t2= 2
t3= 3
t4= 4

data_items= [x1, x2, x3, x4]
C1= [x1, x2]
C2= [x3, x4]
tags= [t1, t2, t3, t4]
T1= [t1, t2]
T2= [t2, t3]
T3= [t3, t4]
T4= [t1, t2]
B= [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
D1= t2
D2= t4

y= [[0, 0], [1, 0], [0, 0], [0, 1]]

N= 4 #number of tags
K= 2 #number of cluster

#minimize the sum of the variables in A
A1= 0
for j in (0, 1, 2, 3):
    for k in (0, 1):
        A1+= y[j][k]

print("Minimize sum of variables: " + str(A1))

#sum of the variables in A should be >= 1
for i in (0, 1, 2, 3):
    A2= 0
    for j in (0, 1, 2, 3):
        if B[i][j]== 1:
            A2+= y[j][k]

print("Sum of variables >=1: " + str(A2))

#sum of the variables in A should be <= alpha
for k in (0, 1):
    A3= 0
    for j in (0, 1, 2, 3):
        A3+= y[j][k]

print("<= alpha: " + str(A3))

#sum of the product terms should be <= beta
for l in (k, 1):
        A4= 0
        for j in (0, 1, 2, 3):
            A4+= (y[j][k] * y[j][l])

print("<= beta: " + str(A4))

print("-------------------")

#GUROBI OPTIMIZATION
import gurobipy as gp
m = gp.Model()

x1 = m.addVar(vtype='B', name="y[j][k]")

#each variable in y(j,k) should take a value from {0,1}
multiplier = 1
for k in (1, K):
    for j in (1, N):
        x_multiplier = m.addVar(vtype='B', name="x_" + str(multiplier))
        multiplier+=1

m.setObjective(A1, gp.GRB.MINIMIZE)

m.optimize()

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: A={A1}")


# #pseudocode for part 2
# # (a)
# for i in (1, x):
#     A = {}
#     for j in (0, N-1):
#         if B[i][j]== 1:
#             A+= y[j][k]
#             print(A)
#
# # (b)
# for i in (1, x):
#     A = {}
#     if B[i][j]== 1:
#         if B[i][j]== 1:
#             A += y[j][k]
#
# (c)
# if y(j,k)=0 OR y(j.l)=0:
#     z(j,k,l)=0
#
# if y(j,k)=1 AND y(j,l)=1:
#     z(j,k,l)=1
#
# (d)
# A= {}
# for j in (1, N):
#     A+= y[j][k][l]
#
# (e)
#     x and y are binary variables