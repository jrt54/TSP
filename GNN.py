import numpy as np
def GNN(A,start):

	path = [start]
	cost = 0
	N = A.shape[0]
	mask = np.ones(N, dtype=bool)
	mask[start] = False

	already_tried = []
	i = 1
	first = True
	while i <= N :
		last = path[-1]
		if i == N :
			check_inf = (A[start,last] != np.inf)
			if check_inf :
				cost += A[start,last]
				path.append(start)
				i += 1
			else:
				i -= 2
				v = path[-2]
				w = path[-3]
				cost -= A[v,w]
				cost -= A[last,v]
				mask[v] = True
				mask[last] = True
				A[v,w] = np.inf
				del path[-1]
				del path[-1]
		else:
			next_ind = np.argmin(A[mask][:,last])
			next_loc = np.arange(A.shape[0])[mask][next_ind]
			check_inf = (A[next_loc,last]!= np.inf)
			check_tried = (next_loc in already_tried)
			if check_inf and not(check_tried) :
				path.append(next_loc)
				mask[next_loc] = False
				cost += A[next_loc,last]
				i += 1
				already_tried = []
			else :
				i -= 1
				if i == 0:
					cost = np.inf
					path = []
					break
				v = path[-2]
				cost -= A[last,v]
				A[last,v] = np.inf
				mask[last] = True
				del path[-1]
				already_tried.append(next_loc)
	return path, cost
