#from gurobipy import *
from sys import argv

filename = "test.txt"
edgeset = []

with open(filename) as input:
  for lines in input:
    edgeset.append(lines.rstrip('\n'))

# for i in range(len(edgeset)):
#   print edgeset[i]
# # print txt.read()


#costvec = multidict({})
costvec = {}

for j in range(1, len(edgeset)):
  begin, end, cost = edgeset[j].split()
  costvec[(begin, end)] = cost
  print(begin, end, cost)

print(('46', '47') in costvec)


#m = Model('netflow')

#m.addConstr(quicksum(flow[h,i,j] for h in commodities) <= capacity[i,j],
# #                 'cap_%s_%s' % (i, j))

# print "Type the filename again:"
# file_again = raw_input("> ")

# txt_again = open(file_again)

# print txt_again.read()



# Model data





# commodities = ['Pencils', 'Pens']
# nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']

# arcs, capacity = multidict({
#   ('Detroit', 'Boston'):   100,
#   ('Detroit', 'New York'):  80,
#   ('Detroit', 'Seattle'):  120,
#   ('Denver',  'Boston'):   120,
#   ('Denver',  'New York'): 120,
#   ('Denver',  'Seattle'):  120 })
# arcs = tuplelist(arcs)

# cost = {
#   ('Pencils', 'Detroit', 'Boston'):   10,
#   ('Pencils', 'Detroit', 'New York'): 20,
#   ('Pencils', 'Detroit', 'Seattle'):  60,
#   ('Pencils', 'Denver',  'Boston'):   40,
#   ('Pencils', 'Denver',  'New York'): 40,
#   ('Pencils', 'Denver',  'Seattle'):  30,
#   ('Pens',    'Detroit', 'Boston'):   20,
#   ('Pens',    'Detroit', 'New York'): 20,
#   ('Pens',    'Detroit', 'Seattle'):  80,
#   ('Pens',    'Denver',  'Boston'):   60,
#   ('Pens',    'Denver',  'New York'): 70,
#   ('Pens',    'Denver',  'Seattle'):  30 }

# inflow = {
#   ('Pencils', 'Detroit'):   50,
#   ('Pencils', 'Denver'):    60,
#   ('Pencils', 'Boston'):   -50,
#   ('Pencils', 'New York'): -50,
#   ('Pencils', 'Seattle'):  -10,
#   ('Pens',    'Detroit'):   60,
#   ('Pens',    'Denver'):    40,
#   ('Pens',    'Boston'):   -40,
#   ('Pens',    'New York'): -30,
#   ('Pens',    'Seattle'):  -30 }

# # # Create optimization model
# # m = Model('netflow')

# # # Create variables
# # flow = {}
# # for h in commodities:
# #     for i,j in arcs:
# #         flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=cost[h,i,j],
# #                                name='flow_%s_%s_%s' % (h, i, j))
# # m.update()

# # # Arc capacity constraints
# # for i,j in arcs:
# #     m.addConstr(quicksum(flow[h,i,j] for h in commodities) <= capacity[i,j],
# #                 'cap_%s_%s' % (i, j))

# # # Flow conservation constraints
# # for h in commodities:
# #     for j in nodes:
# #         m.addConstr(
# #           quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +
# #               inflow[h,j] ==
# #           quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),
# #                    'node_%s_%s' % (h, j))

# # # Compute optimal solution
# # m.optimize()

# # # Print solution
# # if m.status == GRB.Status.OPTIMAL:
# #     for h in commodities:
# #         print '\nOptimal flows for', h, ':'
# #         for i,j in arcs:
# #             if flow[h,i,j].x > 0:
# #                 print i, '->', j, ':', flow[h,i,j].x