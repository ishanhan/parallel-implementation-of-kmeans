import csv, time, random, math
from mpi4py import MPI
import numpy


def eucl_distance(point_one, point_two):
	if(len(point_one) != len(point_two)):
		raise Exception("Error: non comparable points")

	sum_diff = 0.0
	for i in range(len(point_one)):
		diff = pow((float(point_one[i]) - float(point_two[i])), 2)
		sum_diff += diff
	final = math.sqrt(sum_diff)
	return final

def compare_center(initial_center, derived_center, dimensions, num_clusters, cutoff):
	if(len(initial_center) != len(derived_center)):
		raise Exception("Error: non comparable points")

	flag = 0
	for i in xrange(num_clusters):
		diff = eucl_distance(initial_center[i], derived_center[i])
		if(diff < cutoff):
			flag += 1
	return flag


def main():
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	global cutoff, dimensions, num_clusters, data, initial, min_dist
	cutoff = 0.2
	compare_val = 0
	with open('modified_video_game_sales.csv','rb') as f:
			reader = csv.reader(f)
			data = list(reader)
	data.pop(0)
	num_points = len(data)
	dimensions = len(data[0])
	initial = []
	for i in xrange(size):
		initial.append(data[i])
	start_time = time.time()
	while True:	
		# print "initial points",initial, rank
		# print ""
		dist = []
		min_dist = numpy.zeros(num_points)
		for point in data:
			dist.append(eucl_distance(initial[rank], point))

		temp_dist = numpy.array(dist)
		comm.Reduce(temp_dist, min_dist, op = MPI.MIN)
		comm.Barrier()
		if rank == 0:
			min_dist = min_dist.tolist()
		recv_min_dist = comm.bcast(min_dist, root = 0)
		comm.Barrier()
		cluster = []
		for i in xrange(len(recv_min_dist)):
			if recv_min_dist[i] == dist[i]:
				cluster.append(data[i])

		# print "cluster points for",initial[rank]
		# print ""
		# print "cluster points", cluster
		# print ""
		
		center = []
		center_val = [0] * dimensions
		for i in cluster:
			for j in xrange(dimensions):
				center_val[j] += float(i[j])

		for j in xrange(dimensions):
			if(len(cluster) != 0):
				center_val[j] = center_val[j] / len(cluster)





		center = comm.gather(center_val, root = 0)
		comm.Barrier()
		if rank == 0:
		 	compare_val = compare_center(initial, center, dimensions, size, cutoff)
		 	if compare_val == size:
		 		print center
		 		print ("Execution time %s seconds" % (time.time() - start_time))
		break_val = comm.bcast(compare_val, root = 0)

		initial = comm.bcast(center, root = 0)
		comm.Barrier()

		if break_val == size:
			break

	
	MPI.Finalize()



if __name__ == "__main__":
	main()