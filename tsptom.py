from gurobipy import *
import numpy as np

A = np.loadtxt('test.txt', skiprows=1);
N = 4;
Esize = A.shape[0]
V = A[:,:2]
W = A[:,2]

model = Model("TSP")

vars = model.addVars(Esize, vtype=GRB.CONTINUOUS)

model.addConstrs((vars[i] >= 0 for i in range(Esize)), 'c0')
model.addConstrs((vars[i] <= 1 for i in range(Esize)), 'c1')

for i in range(N):
    coefs = np.zeros(Esize)
    for j in range(Esize):
        if (V[j,0]==i) or (V[j,1]==i):
            coefs[j] = 1
        else:
            coefs[j] = 0
    coefsdic = dict(zip(vars,coefs))
    l = vars.prod(coefsdic)
    model.addConstr(l, GRB.EQUAL, 2, 'c')

dic = dict(zip(vars, W))
l = vars.prod(dic)
model.setObjective(l, GRB.MINIMIZE)

model.optimize()

model.write("tomout.sol")
