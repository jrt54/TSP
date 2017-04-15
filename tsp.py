from gurobipy import *
from sys import argv
import operator

#G is dict containing edges mapped to solution weight
def minimumCutPhase(G, start):
  A = [start]
  print(A)
  #gets all edges connecting A to rest of G
  connected = {(i,j):G[i,j] for i,j in G.keys() if (i in A and j not in A) or (j in A and i not in A)}
  for i,j in connected.keys():
    print("wow")
    print(i,j)
  print(connected)
  #selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] > 0.0 and i<j}  

def main():
  filename = "test.txt"
  edgeset = []

  with open(filename) as input:
    for lines in input:
      edgeset.append(lines.rstrip('\n'))

  #V is number of nodes, E is number of edges
  V, E = (int(x) for x in edgeset[0].split())
  print V, E


  
  dist = {}
  #read file and create a dictionary of edge, 
  for j in range(1, len(edgeset)): 
    begin, end, cost = ([float(x) for x in edgeset[j].split()])
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
