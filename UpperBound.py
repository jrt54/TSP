#from gurobipy import *
import sys
import numpy as np
from getTSP_UB import get_UB
from getTSP_UB import display_BestPath
import math
import time

filename = sys.argv[1]
edgeset = []

enhance = int(sys.argv[2])

with open(filename) as input:
  for lines in input:
    edgeset.append(lines.rstrip('\n'))

Nn, Ne = edgeset[0].split()
Nn = int(Nn)
A = np.full((Nn,Nn), np.inf)
for j in range(1, len(edgeset)):
  begin, end, cost = edgeset[j].split()
  begin = int(begin)
  end = int(end)
  cost = float(cost)
  A[begin,end] = cost
  A[end,begin] = cost


#K = 10
#timer = [None]*K
#for k in range(K):
#	start = time.time()
#	bp, bc = get_UB(A,enhance)
#	end = time.time()
#	timer[k] = end - start
#tavg = sum(timer)/K

start = time.time()
bp, bc, z, i, t = get_UB(A,enhance)
end = time.time()
elapsed = end - start
display_BestPath(A,bp,bc)
print
print 'Best path found using GNN from node ', i
print 'Number of Swaps in Enhancement: ', z
print 'Time Elapsed TOTAL: ', elapsed
print 'Time Elapsed SOLUTION NODE: ', t
