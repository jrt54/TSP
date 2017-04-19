import numpy as np
import re

def outputModel(in_name, cost_dict, out_name):

	edgeset = []
	input = open(in_name)
	lines = input.readlines()[2:-2]
	input.close()
	for line in lines:
		line = re.sub('[e\[,\]]',' ', line)
		edge = line.split()
		if int(edge[2]):
			edgeset.append((int(edge[0]),int(edge[1])))
	(i,j) = edgeset[0]
	edgeset = sortIntoPath([edgeset[0]], edgeset[1:])
	N = len(edgeset)
	total_cost = 0
	output = open(out_name, 'w')
	for i in range(N):
		(start, end) = edgeset[i]
		if (start, end) in cost_dict:
			c = cost_dict.get((start,end))
		elif (end,start) in cost_dict:
			c = cost_dict.get((end,start))
		
		to_write = str(start)+'\t'+str(end)+'\t'+str(c)+'\t// for edge('+str(i)+') of tour\n'
		output.write(to_write)
		total_cost = total_cost + c
	to_write = 'The cost of the best tour is: \t' + str(total_cost)
	output.write(to_write )
	output.close()

def sortIntoPath(sort, to_sort):
	if len(sort) == 0:
		return to_sort
	if len(to_sort)==0:
		return sort
	(i0,j0) = sort[-1]
	matches = [item for item in to_sort if j0 in item]
	(i1,j1) = matches[0]
	if i1==j0:
		sort.append(matches[0])
	else:
		sort.append((j1,i1))
	to_sort.remove(matches[0])
	return sortIntoPath(sort, to_sort)

def main():
	filename = 'berlin52.txt'
	edgeset = []
	with open(filename) as input:
		for lines in input:
			edgeset.append(lines.rstrip('\n'))
	DATA = np.loadtxt(filename,skiprows=1)
	EDGES = DATA[:,:2]
	WEIGHTS = DATA[:,2]
	dist = {}
	for j in range(len(edgeset)-2):
		begin = int(EDGES[j,0])
		end = int(EDGES[j,1])
		cost = WEIGHTS[j]
		dist.update({(begin,end): cost})

	in_name = ['TSP/runtimelogs/']
	in_name.append(filename)
	in_name.append('.sol')
	in_name = ''.join(in_name)
	out_name = filename + '.sol.out'
	outputModel(in_name, dist,out_name)

if __name__ == "__main__":
	main()
