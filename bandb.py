from gurobipy import *
from sys import argv
import operator
import numpy as np
import tsp
#G is dict containing edges mapped to solution weight

  #selected = {(i,j):vals[i, j] for i,j in vals.keys() if vals[i,j] > 0.0 and i<j}  


def branch(model):
	currentmodel = model.copy()

  	
  
	#sort them by most promising branch
	
	#if the most promising branch is integral then it is the optimal solution
	currentmodel.optimize()
	tsp.subtour(currentmodel)
	branches = [(currentmodel, currentmodel.objVal)]
	nodesSearched = 1
	isintegral = True
	for v in currentmodel.getVars():
		if not (v.X == 0 or v.X == 1):

			branchingnode = v
			#print v
			isintegral = False
			break

	
	#print(all(isinstance(vals[i, j], int) for i, j in vars.keys()))
  
	#this will be a while loop later, for now we're branching ONCE
	#if the current solution is not integral procee
	while not(isintegral):
		#print branchingnode
		daughter1 = currentmodel.copy()
		boundednode1 = daughter1.getVarByName(branchingnode.VarName)
		#print("before bound:", branchingnode.VarName, branchingnode.X)
		#daughter1 will enforce that a nonintegral edge is 0
		daughter1.addConstr(boundednode1 == 0)		
		daughter1.optimize()
                tsp.subtour(daughter1)
		
		daughter2 = currentmodel.copy()
		boundednode2 = daughter2.getVarByName(branchingnode.VarName)
		#print("before bound:", branchingnode.VarName, branchingnode.X)
		#daughter2 will enforce that a nonintegral edge is 1
		daughter2.addConstr(boundednode2 == 1)
		daughter2.optimize()
                tsp.subtour(daughter2)
                
		if not daughter2.Status == GRB.INFEASIBLE:
			branches.extend([(daughter2, daughter2.objVal)])
		if not daughter1.STATUS == GRB.INFEASIBLE:
			branches.extend([(daughter1, daughter1.objVal)])
		#remove the node from which we branched so that we only search leaves
		branches.remove((currentmodel, currentmodel.objVal))
		branches.sort(key = lambda x: x[1])
		#print branches

		currentmodel = branches[0][0]
		print currentmodel.getVars()

		#print currentmodel.getVars()
		currentmodel.write("bandb.sol")
		isintegral = True
		for v in currentmodel.getVars():
			if not (v.X == 0 or v.X == 1):
				branchingnode = v
				print v
				isintegral = False
				break
		print(isintegral)
		nodesSearched = nodesSearched + 2

	#print ("Branches Searched: ", nodesSearched)	
	return currentmodel, nodesSearched			

	

 


  # #return, best solution is 
  # else
  # daughtermodel = 
  #branch
  #copy model to daughter1 daughter2
  #daughter1.addconstraint(nonintv = 0), etc.
  #take model from branch list
  #repeat
  



def main():
  filename = "hk48.txt"
  edgeset = []

  with open("data/" + filename) as input:

    for lines in input:
      edgeset.append(lines.rstrip('\n'))
  print edgeset

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


  integersol = branch(m)
  currentmodel.write("filename" + ".sol")
  

  
if __name__ == "__main__":
  main()
