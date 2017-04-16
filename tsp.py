from gurobipy import *
from sys import argv
import operator
import numpy as np

#G is dict containing edges mapped to solution weight
def minimumCutPhase(G ,start):
  V = []
  #form list of vertices
  for i,j in G.keys():
    if i not in V:
      V.append(i)
    if j not in V:
      V.append(j)
  A = [start]
  #gets all edges connecting A to rest of G
  while len(V) != len(A):
    connected = {(i,j):G[i,j] for i,j in G.keys() if (i in A and j not in A) or (j in A and i not in A)}
    #print("connected is")
    #print(connected)
    score = {}
    for i,j in connected.keys():
      if i in A and j not in A:
        if j in score.keys():
          score[j] = score[j] + connected[i,j]
        if j not in score.keys():
          score[j] = connected[i,j]
      if j in A and i not in A:
        if i in score.keys():
          score[i] = score[i] + connected[i,j]
        if i not in score.keys():
          score[i] = connected[i,j]
    most_connected = max(score.iteritems(), key=operator.itemgetter(1))[0]
    A.append(most_connected)
  print("min cut generated")
  return A[-2], A[-1]

#finds minimum cut by looping over minimumCutPhase
def minimumCut(G, start):
  print("hi")
  #get all nodes and store in V
  V = []
  for i,j in G.keys():
    if i not in V:
      V.append(i)
    if j not in V:
      V.append(j)
  print(V)
  #initialize merge dictionary
  merge = {}
  for i in V:
    merge[i] = [i]
  print("merge formed")
  print(merge)
  for k in range(3):
    second, last = minimumCutPhase(G, start)
    print("nodes " + str(second) + " and " + str(last) + " will be merged")
    #calculate cut cost
    #merge points in second into last
    
    #update weights and connectivity on edges connected to second and last
    #delete node second

  print("wow")
  
def main():
  filename = "data/berlin52.txt"
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
  selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] >= 0.0 and i<j}

  
  minimumCut(selected, selected.keys()[0][0])
  
  m.write("test.sol")
  
if __name__ == "__main__":
  main()
