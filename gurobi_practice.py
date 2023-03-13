# Name: Keara Polovick
# Computing ID: uzy2ws

alpha= 2
beta= 1

import gurobipy as gp
m = gp.Model()

y1 = m.addVar(vtype='B', name="y1")         #y1,1
y2 = m.addVar(vtype='B', name="y2")         #y1,2
y3 = m.addVar(vtype='B', name="y3")         #y1,3
y4 = m.addVar(vtype='B', name="y4")         #y1,4

y5 = m.addVar(vtype='B', name="y5")         #y2,1
y6 = m.addVar(vtype= 'B', name= "y6")       #y2,2
y7 = m.addVar(vtype= 'B', name= "y7")       #y2,3
y8 = m.addVar(vtype= 'B', name= "y8")       #y2,4
m.update()

m.setObjective(y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8, gp.GRB.MINIMIZE)

m.addConstr(y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 >=1)
m.addConstr(y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 <= alpha)
m.addConstr(y1*y5 + y1*y6 + y1*y7 + y1*y8 + y2*y5 + y2*y6 + y2*y7 + y2*y8 + y3*y5 + y3*y6 + y3*y7 + y3*y8 + y4*y5 + y4*y6 + y4*y7 + y4*y8 + y5*y1 + y5*y2 + y5*y3 + y5*y4 + y6*y1 + y6*y2 + y6*y3 + y6*y4 + y7*y1 + y7*y2 + y7*y3 + y7*y4 + y8*y1 + y8*y2 + y8*y3 + y8*y4 <= beta)

m.optimize()

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: y1={y1.X}, y2={y2.X}, y3={y3.X}, y4={y4.X}, y5={y5.X}, y6={y6.X}, y7={y7.X}, y8={y8.X}")

