import csv, time, random, math
import matplotlib.pyplot as plt
import pandas as pd


colors = ['red', 'green', 'blue','yellow','black']
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


def kmeans(points, num_clusters, cutoff, initial, dimensions):
	
	
	clusters = []
	
	for i in xrange(num_clusters):
		clusters.append([])

	
	for i in points:
		min_val = 10000000000000
		cluster_no = 0
		x = 0
		for j in initial:
			dist = eucl_distance(i,j)
			x = x + 1
			if(dist < min_val):
				min_val = dist
				cluster_no = x
		clusters[cluster_no-1].append(i)


	center = []
	for i in clusters:
		center_val = [0] * dimensions
		no_of_values = 0
		for j in i:
			no_of_values = no_of_values + 1
			for k in xrange(dimensions):
				center_val[k] += float(j[k])
		for m in xrange(dimensions):
			if no_of_values != 0:
				center_val[m] = center_val[m] / no_of_values
		center.append(center_val)

	compare_val = compare_center(initial, center, dimensions, num_clusters, cutoff)
	if(compare_val == num_clusters):
		curX, curY = [], []
		iter_count = 0
		for points in clusters:
			curX, curY = [], []
			for point in points:				
				curX.append(point[4])
				curY.append(point[8])
			plt.scatter(curX,curY,c = colors[iter_count])
			iter_count += 1
		plt.xlabel("Video Game Sales in North America")
    		plt.ylabel("Video Game Sales around Globe")
    		plt.title("Clustering Output")
		plt.savefig("Clustering_Images/clustering_data.png")
		return 1, center
	else:
		return 0, center



def main():
	
	dataset = []
	print "Enter the number of clusters you want to make:"
	num_clusters = raw_input()
	num_clusters = int(num_clusters)
	with open('modified.csv', 'rb') as f:
		reader = csv.reader(f)
		dataset = list(reader)
	data = dataset
	data.pop(0)
	num_points = len(data)
	cutoff = 0.2
	dimensions = len(data[0])
	initial = []
	for i in xrange(num_clusters):
		initial.append(data[i])
	start_time = time.time()
	while(True):
		val, center = kmeans(data, num_clusters, cutoff, initial, dimensions)
		if(val == 1):
		 	break
		initial = center
		i = i + 1

	print "Final Centers are:"
	print center
	print ("Execution time %s seconds" % (time.time() - start_time))

if __name__ == "__main__":
	main()
