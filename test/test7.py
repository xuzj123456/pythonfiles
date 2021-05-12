# coding=utf-8
import numpy as np
import pandas as pd

# a.
df = pd.read_excel('fx_treasury[1319].xls', index_col=0)
df.iloc[:,1]=df.iloc[:,1]/100
df = df.diff()
df.dropna(inplace=True)
A = np.diag(df.std())
B = np.diag([-3.295756,2.96609])
print(2.33*(np.sqrt((A@B@df.corr()@B@A).sum().sum()))*1000000)

# c.
Loss = []
for x, y in np.random.multivariate_normal(mean=df.mean(), cov=df.cov(), size=1000):
    Loss.append(B[0][0]*x+B[1][1]*y)
print(np.percentile(Loss,99)*1000000)

Loss = []
for x, y in np.random.multivariate_normal(mean=df.mean(), cov=df.cov(), size=5000):
    Loss.append(B[0][0]*x+B[1][1]*y)
print(np.percentile(Loss,99)*1000000)

