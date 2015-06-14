###############################################################################
##
##	Ananya Kirti @ June 9 2015
##	Fuzzy C means
##
###############################################################################
## Ananya Kirti


# importing all the required components, you may also use scikit for a direct implementation.
import copy
import math
import random
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import decimal


#used for randomising U
global MAX
MAX = 10000.0
#used for end condition
global Epsilon
Epsilon = 0.00001

def import_data(file):
	"""
	 This function imports the data into a list form a file name passed as an argument. 
	 The file should only the data seperated by a space.(or change the delimiter as required in split)
	"""
	data = []
	f = open(str(file), 'r')
	for line in f:
		current = line.split()	#enter your own delimiter like ","
		for j in range(0,len(current)):
			current[j] = int(current[j])
		data.append(current)
	print "finished importing data"
	return data

def import_data_format_iris(file):
	""" 
	This would format the data as required by iris 
	the link for the same is http://archive.ics.uci.edu/ml/machine-learning-databases/iris/
	"""
	data = []
	cluster_location =[]
	f = open(str(file), 'r')
	for line in f:
		current = line.split(",")
		current_dummy = []
		for j in range(0,len(current)-1):
			current_dummy.append(float(current[j]))
		j+=1 
		#print current[j]
		if  current[j] == "Iris-setosa\n":
			cluster_location.append(0)
		elif current[j] == "Iris-versicolor\n":
			cluster_location.append(1)
		else:
			cluster_location.append(2)
		data.append(current_dummy)
	print "finished importing data"
	return data , cluster_location

def randomise_data(data):
	"""
	This function randomises the data, and also keeps record of the order of randomisation.
	"""
	order = range(0,len(data))
	random.shuffle(order)
	new_data = [[] for i in range(0,len(data))]
	for index in range(0,len(order)):
		new_data[index] = data[order[index]]
	return new_data, order

def de_randomise_data(data, order):
	"""
	This function would return the original order of the data, pass the order list returned in randomise_data() as an argument
	"""
	new_data = [[]for i in range(0,len(data))]
	for index in range(len(order)):
		new_data[order[index]] = data[index]
	return new_data

def print_matrix(list):
	""" 
	Prints the matrix in a more reqdable way
	"""
	for i in range(0,len(list)):
		print list[i]

def end_conditon(U,U_old):
	"""
	This is the end conditions, it happens when the U matrix stops chaning too much with successive iterations.
	"""
	global Epsilon
	for i in range(0,len(U)):
		for j in range(0,len(U[0])):
			if abs(U[i][j] - U_old[i][j]) > Epsilon :
				return False
	return True

def initialise_U(data, cluster_number):
	"""
	This function would randomis U such that the rows add up to 1. it requires a global MAX.
	"""
	global MAX
	U = []
	for i in range(0,len(data)):
		current = []
		rand_sum = 0.0
		for j in range(0,cluster_number):
			dummy = random.randint(1,int(MAX))
			current.append(dummy)
			rand_sum += dummy
		for j in range(0,cluster_number):
			current[j] = current[j] / rand_sum
		U.append(current)
	return U

def distance(point, center):
	"""
	This function calculates the distance between 2 points (taken as a list). We are refering to Eucledian Distance.
	"""
	if len(point) != len(center):
		return -1
	dummy = 0.0
	for i in range(0,len(point)):
		dummy += abs(point[i] - center[i]) ** 2
	return math.sqrt(dummy)

def normalise_U(U):
	"""
	This de-fuzzifies the U, at the end of the clustering. It would assume that the point is a member of the cluster whoes membership is maximum.
	"""
	for i in range(0,len(U)):
		maximum = max(U[i])
		for j in range(0,len(U[0])):
			if U[i][j] != maximum:
				U[i][j] = 0
			else:
				U[i][j] = 1
	return U

def checker_iris(final_location):
	"""
	This is used to find the percentage correct match with the real clustering.
	"""
	right = 0.0
	for k in range(0,3):
		checker =[0,0,0]
		for i in range(0,50):
			for j in range(0,len(final_location[0])):
				if final_location[i + (50*k)][j] == 1:
					checker[j] += 1
		right += max(checker)
		print right
	answer =  right / 150 * 100
	return answer

def color(cluster_number):
	colors = []
	for i in range(0,cluster_number):
		colors.append("#%06x" % random.randint(0,0xFFFFFF))
	return colors

def animate(data, U, cluster_number, colors):
	#plt.close("all")
	cluster = [[]for i in range(0,cluster_number)]
	for i in range(0,len(U)):
		for j in range(0,cluster_number): 
			if U[i][j] == 1:
				cluster[j].append(data[i])

	#colors = ['ro', 'bs', 'wa', 'ga', 'ys']
	plt.ion()
	plt.figure()
	for i in range(0,cluster_number):
		x_list_0 = [x for [x, y] in cluster[i]]
		y_list_0 = [y for [x, y] in cluster[i]]
		plt.plot(x_list_0, y_list_0 , colors[i] , marker='o', ls='')
		#print i
	plt.gca().set_aspect('equal', adjustable='box')
	plt.axis('equal')
	plt.show(block=False)
	time.sleep(.5)






def fuzzy(data, cluster_number, m = 2 ):
	"""
	This is the main function, it would calculate the required center, and return the final normalised membership matrix U.
	It's paramaters are the : cluster number and the fuzzifier "m".
	"""
	## initialise the U matrix:
	U = initialise_U(data, cluster_number)
	print cluster_number
	colors = color(cluster_number)
	plt.axis([0, 15, 0, 15])
	plt.ion()
	plt.show(block=False)
	animate(data, normalise_U(copy.deepcopy(U)),cluster_number,colors)

	#print_matrix(U)
	#initilise the loop
	while (True):
		#create a copy of it, to check the end conditions
		U_old = copy.deepcopy(U)
		# cluster center vector
		C = []
		for j in range(0,cluster_number):
			current_cluster_center = []
			for i in range(0,len(data[0])): #this is the number of dimensions
				dummy_sum_num = 0.0
				dummy_sum_dum = 0.0
				for k in range(0,len(data)):
					dummy_sum_num += (U[k][j] ** m) * data[k][i]
					dummy_sum_dum += (U[k][j] ** m)
				current_cluster_center.append(dummy_sum_num/dummy_sum_dum)
			C.append(current_cluster_center)

		#creating a distance vector, useful in calculating the U matrix.

		distance_matrix =[]
		for i in range(0,len(data)):
			current = []
			for j in range(0,cluster_number):
				current.append(distance(data[i], C[j]))
			distance_matrix.append(current)

		# update U vector
		for j in range(0, cluster_number):	
			for i in range(0, len(data)):
				dummy = 0.0
				for k in range(0,cluster_number):
					dummy += (distance_matrix[i][j]/ distance_matrix[i][k]) ** (2/(m-1))
				U[i][j] = 1 / dummy

		animate(data, normalise_U(copy.deepcopy(U)),cluster_number,colors)
		if end_conditon(U,U_old):
			print "finished clustering"
			break
	U = normalise_U(U)
	print "normalised U"
	return U

## main 
if __name__ == '__main__':
	
	# import the data
	data = import_data(str(sys.argv[1]))
	#data, cluster_location = import_data_format_iris("iris.txt")
	#print_matrix(data)
	#data , order = randomise_data(data)
	#print_matrix(data)

	start = time.time()
	# now we have the data in a list called data, this is only number
	# also we have another list called the cluster location, which gives the right cluster location
	# call the fuzzy - c means function
	final_location = fuzzy(data , 9, 2)
	#final_location = de_randomise_data(final_location, order)
	#print_matrix(final_location)
	#print checker_iris(final_location)
	#print "time elapsed=", time.time() - start
