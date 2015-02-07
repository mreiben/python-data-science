import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors
import math
from collections import Counter

#load csv
irisData = pd.read_csv('http://aima.cs.berkeley.edu/data/iris.csv')

#set column titles
irisData.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

#show scatter plot of sepal length and width
# plt.scatter(irisData['sepal_length'], irisData['sepal_width'])
# plt.show()

#choose random sepal length and width for test data
random_width = np.random.uniform(1.5, 4.5)
random_length = np.random.uniform(4.0, 8.0)

#create empty column for distance between known data points and test data
irisData['distance'] = ""

#function for determining distance between test data and training data
def distance(a_x, a_y, b_x, b_y):
	return math.sqrt(((a_x - b_x)**2) + ((a_y - b_y)**2))

#iterate over the set to find the distance between each data point and the test data
for i in range(len(irisData.index)):
	irisData['distance'][i] = distance(random_length, random_width, irisData['sepal_length'][i], irisData['sepal_width'][i])

#choose the 10 (k) nearest neighbors based on distance
# nearest_10 = irisData.sort('distance', ascending=True)[0:10]
#
# class_count = Counter(nearest_10['class']).most_common()
#
# majority_class = class_count[0][0]
#
# print majority_class

#function for finding k nearest neighbors
def knn(k):
	data = irisData.sort('distance', ascending=True)[0:k]
	class_count = Counter(data['class']).most_common()
	return class_count[0][0]

print "Based on the ten nearest neighbors, n iris with a sepal width of", random_width, "and a sepal length of", random_length, "is most likely a", knn(10), "iris!"
