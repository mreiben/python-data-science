import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors
import math
from collections import Counter

#load csv
unData = pd.read_csv('un.csv')

print unData[0:1]

print "number of rows: ", len(unData.index)

for column in unData:
    print "Non-null values in ", column, "= ", unData[column].count()
