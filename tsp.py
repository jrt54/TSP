from gurobipy import *
from sys import argv

filename = "test.txt"
edgeset = []

with open(filename) as input:
  for lines in input:
    edgeset.append(lines.rstrip('\n'))

#V is number of nodes, E is number of edges
V, E = (int(x) for x in edgeset[0].split())
print V, E

print edgeset[1].split()


dist = {}




#  begin, end, cost = edgeset[j].split()
#  begin, end, cost = ([float(x) for x in edgeset[j].split()])
#  begin, end, cost = int(edgeset[j].split()[0]), int(edgeset[j].split()[1]), float(edgeset[j].split()[2])

dist = {}
#read file and create a dictionary of edge, 
for j in range(1, len(edgeset)): 
  print j
  begin, end, cost = ([float(x) for x in edgeset[j].split()])
  dist.update({(begin, end): cost})

#print dist

#print((int(46), int(47)) in weight)



m = Model()


#creates variable x_i,j from 0 to 1 corresponding to whether an edge is traversed or not.
#creates corresponding cost coefficient for the weight on that edge 

#could also use:
#vars = tupledict()
#for i,j in dist.keys():
#   vars[i,j] = m.addVar(lb = 0.0, ub = 1.0, obj=dist[i,j], vtype=GRB.CONTINUOUS,                       name='e[%d,%d]'%(i,j))

#for i, j in vars.keys():
#   vars[j, i] = vars[i, j]


vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i,j in vars.keys():
	 vars[j,i] = vars[i,j] # edge in opposite direction


# Add degree-2 constraint, each node is entered and exited
m.addConstrs(vars.sum(i,'*') == 2 for i in range(V))


m.update()

m._vars = vars
#m.Params.lazyConstraints = 1
#m.optimize(subtourlim)
m.optimize()

vals = m.getAttr('x', vars)
selected = tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.0)
print(selected)


m.write("test.sol")
#print('')
#print('Optimal tour: %s' % str(tour))
#print('Optimal cost: %g' % m.objVal)
#print('')


##find subtour out of list of edges
##we have to modify this function

## Given a tuplelist of edges, find the shortest subtour

# def subtour(edges):
#     unvisited = list(range(n))
#     cycle = range(n+1) # initial length has 1 more city
#     while unvisited: # true if list is non-empty
#         thiscycle = []
#         neighbors = unvisited
#         while neighbors:
#             current = neighbors[0]
#             thiscycle.append(current)
#             unvisited.remove(current)
#             neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
#         if len(cycle) > len(thiscycle):
#             cycle = thiscycle
#     return cycle



# def subtourelim(model, where):
#     if where == GRB.Callback.MIPSOL:
#         # make a list of edges selected in the solution
#         vals = model.cbGetSolution(model._vars)
#         selected = tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
#         # find the shortest cycle in the selected edge list
#         tour = subtour(selected)
#         if len(tour) < n:
#             # add subtour elimination constraint for every pair of cities in tour
#             model.cbLazy(quicksum(model._vars[i,j]
#                                   for i,j in itertools.combinations(tour, 2))
#                          <= len(tour)-1)

##tour = subtour(selected)
##assert len(tour == n)


##could also use:
## vars = tupledict()
## for i,j in dist.keys():
##   vars[i,j] = m.addVar(lb = 0.0, ub = 1.0, obj=dist[i,j], vtype=GRB.CONTINUOUS,
##                       name='e[%d,%d]'%(i,j))





# # Using Python looping constructs, 
# #
# # for i in range(n):
# #   m.addConstr(sum(vars[i,j] for j in range(V)) == 2)
