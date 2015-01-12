import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import collections

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines']) #count frequency of different values of open credit lines

plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

chi, p = stats.chisquare(freq.values())
print "chi is " + str(chi)
print "p is " + str(p)
