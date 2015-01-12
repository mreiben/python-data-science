import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

df = pd.read_csv('LoanStats3a.csv', header=1, low_memory=False)
# converts string to datetime object in pandas:
df['list_d_format'] = pd.to_datetime(df['issue_d'])

dfts = df.set_index('list_d_format')

year_month_summary = dfts.groupby(lambda x : x.year*100+x.month).count()

loan_count_summary = year_month_summary['issue_d']

a = sm.graphics.tsa.plot_acf(loan_count_summary)
plt.show()
plt.close()

a = sm.graphics.tsa.plot_pacf(loan_count_summary)
plt.show()
plt.close()