import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.cluster import KMeans
import math
from collections import Counter
import random

for i in range(10):
    if(random.random() < .5):
        print "head"
    else:
        print "tail"
