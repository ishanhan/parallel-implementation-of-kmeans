import csv, time, random, math
from mpi4py import MPI


def eucl_distance(point_one, point_two):
	if(len(point_one) != len(point_two)):
		raise Exception("Error: non comparable points")

	sum_diff = 0.0
	for i in range(len(point_one)):
		diff = pow((float(point_one[i]) - float(point_two[i])), 2)
		sum_diff += diff
	final = math.sqrt(sum_diff)
	return final


def main():
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()	
	global cutoff, dimensions, dataset, num_clusters, data
	
	if rank == 0:
		print "Enter the number of clusters you want to make:"
		num_clusters = raw_input()
		num_clusters = int(num_clusters)
		with open('test.csv', 'rb') as f:
			reader = csv.reader(f)
			dataset = list(reader)
		initial = []
		dataset.pop(0)		
		data = dataset
		for i in xrange(num_clusters):
			initial.append(dataset[i])
		#	dataset.pop(0)
		num_points = len(dataset)
		dimensions = len(dataset[0])
	else:
		initial = None
		data = None 	
	cutoff = 0.2
	loop = 0
	compare_cutoff = True
	while compare_cutoff:
		loop += 1	
		clusters = []
		strpt = comm.bcast(initial, root = 0)
		recv = comm.scatter( data,	 root = 0)
		least = eucl_distance(strpt[0], recv)
		for i in xrange(len(strpt)):
			clusters.append([])	
		lpoint = 0
		for i in xrange(len(strpt)):
			a = eucl_distance(strpt[i], recv)
			if a < least :
				least = a
				lpoint = i
	 	clusters[lpoint]= recv	
		fc = comm.gather(clusters, root = 0)
		if rank == 0:
			nfc = []
			no = []
			for i in xrange(len(initial)):
				nfc.append(['0', '0'])
				no.append('0')
			for i in xrange(len(fc)):
				for j in xrange(len(fc[i])):
					if len(fc[i][j]) != 0:
						no[j] = int(no[j]) + 1
						for k in xrange(len(fc[i][j])):
							nfc[j][k] = float(nfc[j][k]) + float(fc[i][j][k])				
							
									
			for i in xrange(len(nfc)):
				for j in xrange(len(nfc[i])):
					nfc[i][j] = float(nfc[i][j]) / float(no[i])
			flag = 0		
			for i in xrange(len(nfc)):
				if eucl_distance(nfc[i], initial[i]) > cutoff:
					flag += 1
			if flag == 0:
				compare_cutoff = False
				print nfc
				compare_cutoff = comm.bcast(compare_cutoff, root = 0)
				print fc			
				print ("Execution time %s seconds" % (time.time() - start_time))
				print loop
			else:
				initial = nfc
	MPI.Finalize()		
	exit(0)	
if __name__ == "__main__":
	start_time = time.time()
	main()
	
