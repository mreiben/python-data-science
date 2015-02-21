import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.cluster import KMeans
import math
from collections import Counter

#load csv
unData = pd.read_csv('un.csv')

# print unData[0:1]
#
# print "number of rows: ", len(unData.index)
#
# for column in unData:
#     print "Non-null values in ", column, "= ", unData[column].count()

unData = unData[['country','lifeMale', 'lifeFemale', 'infantMortality', 'GDPperCapita']].dropna()

print unData[0:4]

#fit the data into clusters, using GDPperCapita as the dependent variable
kmeans_model = KMeans(n_clusters=3, random_state=1).fit(unData[['lifeFemale', 'GDPperCapita']])

#add cluster labels to the data set
unData['label'] = kmeans_model.labels_

plt.scatter(x=unData['GDPperCapita'], y=unData['lifeFemale'], c=unData["label"])
plt.show()
plt.clf()
