# Name: Keara Polovick
# Computing ID: uzy2ws

import gurobipy as gp
m = gp.Model()

x1 = m.addVar(vtype='B', name="x1")
x2 = m.addVar(vtype='B', name="x2")
x3 = m.addVar(vtype='B', name="x3")
x4 = m.addVar(vtype='B', name="x4")
x5 = m.addVar(vtype='B', name="x5")
x6= m.addVar(vtype= 'B', name= "x6")

m.setObjective(15*x1 + 20*x2 + 25*x3 + 12*x4 + 10*x5 + 20*x6, gp.GRB.MAXIMIZE)

m.addConstr(5*x1 + 6*x2 + 7*x3 + 11*x4 + 13*x5 + 20*x6 <=18)

m.optimize()

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x1={x1.X}, x2={x2.X}, x3={x3.X}, x4={x4.X}, x5={x5.X}, x6={x6.X}")
