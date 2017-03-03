import random

def make_rand_point(n, lower, upper):
	p = ([random.uniform(lower, upper) for _ in range(n)])
	return p

num_points = 16000
dimensions = 3
lower = 0
upper = 2010
init_cent = [make_rand_point(dimensions, lower, upper) for i in xrange(num_points)]
print init_cent