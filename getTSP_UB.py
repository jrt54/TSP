import numpy as np
import time
from GNN import GNN
from enhance import enhance_2opt
from enhance import enhance_3opt

def get_UB(M,e) :
	A = np.copy(M)
	N = A.shape[0]
	best_node = -1 
	best_cost = np.inf
	best_path = []
	best_z = 0
	for i in range(N) :
		start = time.time()
		p,c = GNN(A,i)
		z = 0
		if c != np.inf :
			if e == 2 :
				p,c,z = enhance_2opt(p,c,A,-1)
			if e == 3 :
				p,c,z = enhance_3opt(p,c,A,-1)
			if e == 23 :
				p,c,z = enhance_2opt(p,c,A,-1)
				p,c,z2 = enhance_3opt(p,c,A,-1)
				z = z+z2

		end = time.time()
		elapsed = end - start
		if ((c < best_cost) or ((c == best_cost) and (z < best_z))) :
			best_cost = c
			best_path = p
			best_z = z
			best_node = i
			best_time = elapsed
	return best_path, best_cost, best_z, best_node, best_time

def display_BestPath(A,bp,bc) :
	print(' ')
	if bc == np.inf :
		print('There is no TSP path')
	else:
	   N = len(bp)
           for i in range(N-1):
                print bp[i], '\t', bp[i+1], '\t',  A[bp[i+1],bp[i]], '\t// for edge(',i,') of tour'
           print 'The cost of the best tour is: \t', bc
        return

