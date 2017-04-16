from gurobipy import *
from sys import argv
import operator
import numpy as np

#G is dict containing edges mapped to solution weight

  #selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] > 0.0 and i<j}  

def branch(model, where):
  mother = model.copy()
  motheropt = model.objVal
  branches = [(mother, motheropt)]
  
  #sort them by most promising branch
  sorted(branches, key=lambda x: x[1])
  #if the most promising branch is integral then it is the optimal solution
  currenthead = branches[0]
  currentmodel = currenthead[0] 
  currentmodel.optimize()
  #currentmodel.getAttr(GRB.Attr.x, currentmodel.getVars())
  m._vars = vars
  vals = currentmodel.getAttr('x', vars)
  print(if all(isinstance(vals[i, j], int) for i, j in vals.keys()))

  # #return, best solution is 
  # else
  # daughtermodel = 
  #branch
  #copy model to daughter1 daughter2
  #daughter1.addconstraint(nonintv = 0), etc.
  #take model from branch list
  #repeat
  #



def main():
  filename = "data/att48.txt"
  edgeset = []

  with open(filename) as input:
    for lines in input:
      edgeset.append(lines.rstrip('\n'))

  #V is number of nodes, E is number of edges
  V, E = (int(x) for x in edgeset[0].split())

  DATA = np.loadtxt(filename, skiprows=1)
  EDGES = DATA[:,:2]
  WEIGHTS = DATA[:,2]

  print V, E
  
  dist = {}
  #read file and create a dictionary of edge, 
  for j in range(len(edgeset)-2):
    begin = int(EDGES[j,0])
    end   = int(EDGES[j,1])
    cost  = WEIGHTS[j]
    #begin, end, cost = ([float(x) for x in edgeset[j].split()])
    dist.update({(begin, end): cost})


  #create model
  m = Model()
  #add variables for each edge to model
  vars = m.addVars(dist.keys(), ub = 1, lb = 0, obj=dist, vtype=GRB.CONTINUOUS, name='e')
  for i,j in vars.keys():
    vars[j,i] = vars[i,j] #edge (i,j) same as edge (j,i)

  # Add degree-2 constraint, each node is entered and exited
  m.addConstrs(vars.sum(i,'*') == 2 for i in range(V))

  m._vars = vars
  m.Params.lazyConstraints = 1

  m.optimize()
  
  vals = m.getAttr('x', vars)
  #select edges where solution > 0. specify i<j to remove duplicates
  selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] > 0.0 and i<j}

  
  minimumCutPhase(selected, selected.keys()[0][0])
  
  m.write("test.sol")
  
if __name__ == "__main__":
  main()
