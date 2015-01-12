import matplotlib.pyplot as plt
import collections
import numpy as np
import scipy.stats as stats

#data set
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

c = collections.Counter(x) #counts how many times each number is in the set

count_sum = sum(c.values()) #counts all items

#print out the frequency of each item
for k,v in c.iteritems():
	print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

#create and save a box plot of the data
plt.boxplot(x)
plt.savefig("prob_boxplot.png")
plt.close()

#create and save a histogram of the data
plt.hist(x, histtype="bar")
plt.savefig("prob_hist.png")
plt.close()

#create and save a qq-plot of the data
plt.figure()
graph1 = stats.probplot(x, dist="norm", plot=plt)
plt.savefig("prob_qq.png")
plt.close()