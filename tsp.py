from gurobipy import *
from sys import argv
import operator
import numpy as np
import re
import bandb

#G is dict containing edges mapped to solution weight
def minimumCutPhase(G ,start):
  V = []
  #print(G)
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
  #print("min cut generated")
  return A[-2], A[-1]

#finds minimum cut by looping over minimumCutPhase
def minimumCut(G, start):
  Gorig = G.copy()
  #print("hi")
  #get all nodes and store in V
  V = []
  for i,j in G.keys():
    if i not in V:
      V.append(i)
    if j not in V:
      V.append(j)
  #print(V)
  #initialize merge dictionary
  merge = {}
  for i in V:
    merge[i] = [i]
  #print("merge formed")
  #print(merge)
  minCost = -1
  while len(merge.keys()) > 1:
    second, last = minimumCutPhase(G, start)
    #print("nodes " + str(second) + " and " + str(last) + " will be merged")
    #calculate cut cost
    cost = 0
    cut = {}
    for i,j in Gorig.keys():
      if i in merge[last] and j not in merge[last]:
        cost += Gorig[i,j]
        cut[i,j] = Gorig[i,j]
      if j in merge[last] and i not in merge[last]:
        cost += Gorig[i,j]
        cut[i,j] = Gorig[i,j]
    if minCost<0:
      minCost = cost
      minCut = cut
      minMerge = merge.copy()[last]
    elif cost < minCost:
      minCost = cost
      minCut = cut
      minMerge = merge.copy()[last]
      
    #update merge dictionary
    merge[last] += merge[second]
    del merge[second]
    #update weights and connectivity on edges connected to second and last
    #find things connected to second
    connected = {(i,j):G[i,j] for i,j in G.keys() if (i in [second] and j not in [second]) or (j in [second] and i not in [second])}
    #print("things connected to node second (" + str(second) + ")")
    #print(connected)
    for i,j in connected.keys():
      #delete edge between second,last
      #if i==last:
      #del connected[i,j]
      #if j==last:
      #del connected[i,j]
      if i==second:
        if (j,last) in G.keys():
          G[j,last] += G[i,j]
        elif (last,j) in G.keys():
          G[last,j] += G[i,j]
        elif j<last:
          G[j,last] = G[i,j]
        elif last<j:
          G[last,j] = G[i,j]
      if j==second:
        if (i,last) in G.keys():
          G[i,last] += G[i,j]
        elif (last,i) in G.keys():
          G[last,i] += G[i,j]
        elif i<last:
          G[i,last] = G[i,j]
        elif last<i:
          G[last,i] = G[i,j]
      del G[i,j]
  #print("wow")
  #print("the minimum cut is")
  #print(minCut)
  #print("min cut cost")
  #print(minCost)
  #print("and merge")
  #print(minMerge)
  return minCost, minCut

def testMinCut():
  filename = "data/stoer-wagner-ex.txt"
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

  minimumCut(dist, 1)

def subtour(m):
  m.optimize()

  variables = m.getVars()
  vars = {(map(int, re.findall(r'\d+', i.getAttr(GRB.Attr.VarName)))[0], map(int, re.findall(r'\d+', i.getAttr(GRB.Attr.VarName)))[1]):i for i in variables}
  minCost = 0
  k = 0
  while minCost + 1e-10<2:
    m.optimize()
  
    vals = m.getAttr('x', vars)
    #select edges where solution > 0. specify i<j to remove duplicates
    selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] >= 0.0 and i<j}
    
    minCost, minCut = minimumCut(selected, selected.keys()[0][0])
    print("min cost")
    print(minCost)
    if(minCost<2):
      expr = LinExpr(np.ones(len(minCut.keys())), [vars[i,j] for i,j in minCut.keys()])
      m.addConstr(expr, GRB.GREATER_EQUAL, 2)
    #minimumCut(vars, vars.keys()[0][1])
  return m
  
def nonblank_lines(f):
	for l in f:
		line = l.rstrip()
		if line:
			yield line

def main():
  filename = raw_input("Please enter the filename of the TSP problem (e.g. att48.txt): ") or "att48.txt"
  filename = "data/" + filename

  edgeset = []

  with open(filename) as input:
    for lines in input:
	if not lines.strip()== '':        
		edgeset.append(lines.rstrip('\n'))

  #V is number of nodes, E is number of edges
  print edgeset
  print edgeset[0]
  print edgeset[1]

  
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
  print("vars")
  m.optimize()
  print("NAME")
  #print(m.getVars()[0].getAttr(GRB.Attr.VarName)[3:-1])
  #m = subtour(m)
  integersol = bandb.branch(m)
  integersol.write("filename" + ".sol")
  

if __name__ == "__main__":
  main()
