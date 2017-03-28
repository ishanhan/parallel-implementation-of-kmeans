import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

colors = ['red', 'green', 'blue', 'yellow']

def make_initial_graph():
	data = pd.read_csv('modified.csv', header = 0)
	Y = data['Global_Sales']
    	X = data['NA_Sales']
    	plt.scatter(X, Y, c = 'black')
    	plt.xlabel("Video Game Sales in North America")
    	plt.ylabel("Video Game Sales around the Globe")
    	plt.title("Initial Output")
	plt.savefig("Clustering_Images/Initial.png")

if __name__ == "__main__":
	make_initial_graph()
