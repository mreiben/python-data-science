import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

#retrieve data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.dropna(inplace=True) #remove rows with null values

loansData.boxplot(column='Amount.Requested') #create box plot for amount requested
plt.savefig("amount_requested_box.png")
plt.close()

loansData.hist(column='Amount.Requested') #create histogram for amount requested
plt.savefig("amount_requested_hist.png")
plt.close()

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist='norm', plot=plt) #create qq for amount requested
plt.savefig("amount_requested_qq")
plt.close()