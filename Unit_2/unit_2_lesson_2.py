import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

#retrieve data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.dropna(inplace=True) #remove rows with null values

loansData.boxplot(column='Amount.Funded.By.Investors') #create box plot of amount funded

plt.show()
plt.close()

loansData.hist(column='Amount.Funded.By.Investors')
plt.show()
plt.close()

plt.figure()
graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist='norm', plot=plt)
plt.show()
plt.close()