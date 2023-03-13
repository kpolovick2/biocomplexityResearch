# Name: Keara Polovick
# Computing ID: uzy2ws

import math
import random

from gurobipy import LinExpr, Model


def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def make_data(n):
    x = [random.random() for i in range(n)]
    y = [random.random() for i in range(n)]
    c = {}
    for i in range(n):
        for j in range(n):
            c[i,j] = distance(x[i],y[i],x[j],y[j])
    return c, x, y


import gurobipy as gp
model = gp.Model()

def kmedian(m, n, c, k):
    model = Model("k-median")
    y= {}
    x= {}

    for j in range(m):
        y[j] = model.addVar(obj=0, vtype="B", name="y[%s]"%j)
        for i in range(n):
            x[i, j] = model.addVar(obj= c[i,j], vtype="B", name="x[%s,%s]" %(i, j))
        #model.update()

    for i in range(n):
        coef = [1 for j in range(m)]
        var = [x[i,j] for j in range(m)]
        model.addConstr(LinExpr(coef,var), "=", 1, name="Assign[%s]"%i)

    for j in range(m):
        for i in range(n):
            model.addConstr(x[i,j], "<=", y[j], name="Strong[%s,%s]"%(i,j))

    coef = [1 for j in range(m)]
    var = [y[j] for j in range(m)]
    model.addConstr(LinExpr(coef,var), "=", rhs=k, name="k_median")

    model.update()
    model.__data = x,y
    return model


n = 3
c, x_pos, y_pos = make_data(n)
m = 2
k = 2
model = kmedian(m, n, c, k)
model.optimize()
x,y = model.__data
edges = [(i,j) for (i,j) in x if x[i,j].X == 1]
nodes = [j for j in y if y[j].X == 1]
print("Optimal value=", model.ObjVal)
print("Selected nodes:", nodes)
print("Edges:", edges)