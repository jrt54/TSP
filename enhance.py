import numpy as np
import copy

def enhance_2opt(path, cost, A, z) :
	z = z+1
	N = len(path)
	best_indx = [np.inf] *2
	best_opt = np.inf
	for i in range(N-3) :
		node0 = path[i]
		node1 = path[i+1]
		for j in range(N-i-3):
			node2 = path[i+j+1]
			node3 = path[i+j+2]
			old_sum = A[node3,node2] + A[node1,node0]
			new_sum = A[node2,node0] + A[node3,node1]
			if (new_sum - old_sum < best_opt) :
				best_indx[0] = i
				best_indx[1] = j
				best_opt = new_sum - old_sum
	if (best_opt < 0):
		i = best_indx[0]
		j = best_indx[1]
		path_new = copy.deepcopy(path)
		path_new[i+1:i+2+j] = path[i+j+1:i:-1]
		cost_new = cost + best_opt
		return enhance_2opt(path_new, cost_new, A, z)

	return path,cost,z

def enhance_3opt(path, cost, A, z) :
	z = z+1
	N = len(path)
	best_indx = [np.inf] *3
	best_opt = np.inf
	best_type = -1
	for i in range(N-1):
		node0 = path[i]
		node1 = path[i+1]
		for j in range(N-i-2):
			node2 = path[i+j+1]
			node3 = path[i+j+2]
			for k in range(N-i-j-3):
				node4 = path[i+j+k+2]
				node5 = path[i+j+k+3]
				old_sum = A[node1,node0] + A[node3,node2] + A[node5,node4]
				choices = [np.inf] *3
				choices[0] = A[node3,node0] + A[node1,node4] + A[node5,node2]	
				choices[1] = A[node5,node2] + A[node1,node3] + A[node4,node0]
				choices[2] = A[node5,node1] + A[node2,node4] + A[node3,node0]
				new_sum = min(choices)
				if (new_sum - old_sum < best_opt):
					best_indx[0] = i
					best_indx[1] = j
					best_indx[2] = k
					if (new_sum == choices[0]):
						best_type = 0
					elif (new_sum == choices[1]):
						best_type = 1
					else :
						best_type = 2
					best_opt = new_sum - old_sum

	if (best_opt < 0):
		i = best_indx[0]
		j = best_indx[1]
		k = best_indx[2]
		path_new = copy.deepcopy(path)
		segment = []
		if (best_type == 0):
			segment.extend(path[i+j+2:i+j+k+3])
			segment.extend(path[i+1:i+j+2])
		elif (best_type == 1):
			segment.extend(path[i+j+k+2:i+j+1:-1])
			segment.extend(path[i+1:i+j+2])
		else :
			segment.extend(path[i+j+2:i+j+k+3])
			segment.extend(path[i+j+1:i:-1])
		path_new[i+1:i+j+k+3] = copy.deepcopy(segment)
		cost_new = cost + best_opt
		return enhance_3opt(path_new, cost_new, A, z)

	return path, cost, z
