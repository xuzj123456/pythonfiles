# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Computing and saving the sample average
data_list=[]
for j1 in range(1,10001):
    Xi=np.random.chisquare(5,100)
    average_Xi=Xi.mean()
    data_list.append(average_Xi)
sample=np.array(data_list)
#Computing the min, 25%, 50% and 75% quantiles, max, and the average of the sample
df=pd.DataFrame(sample,columns=['分布'])
df.describe()
#Plotting the histogram of the sample averages and the curve of the normal density
plt.xlim([4,6])
plt.hist(sample,100,density=True,color='green')
plt.title('the Histogram of Sample')
plt.xlabel('Value')
plt.ylabel('Frequencies')

from scipy.stats import norm
domain=np.linspace(0,10,10000)
plt.plot(domain,norm.pdf(domain,df.mean(),df.std()))
plt.show()


data_list2=[]
for j2 in range(1,10001):
    xi=np.random.chisquare(5,100)
    ui=np.random.normal(0,1,100)
    beta=1+sum([xi[i]*ui[i] for i in range(100)])/sum([xi[i]*xi[i] for i in range(100)])
    data_list2.append(beta)
betas=np.array(data_list2)
print(betas)
plt.xlim([0.9,1.1])
df2=pd.DataFrame(betas,columns=['分布'])
print(df2.describe())
plt.hist(betas,1000,density=True,color='red')
plt.show()

from scipy.stats import norm, f
domain=np.linspace(0,10,10000)
plt.plot(domain,norm.pdf(domain,df2.mean(),df2.std()))
plt.show()

from scipy.stats import norm
domain=np.linspace(0,10,10000)
plt.plot(domain,f.pdf(domain,df2.mean(),df2.std()))
plt.show()

s2=0
m2=0
data_list2=[]
for j2 in range(1,10001):
    for i in range(1,101):
        np.random.seed(np.random.randint(10000))
        xi=np.random.chisquare(5,1)
        ui=np.random.normal(0,1,1)
        yi=xi+ui
        s2+=xi*yi
        m2+=xi**2
    beta=s2/m2
    data_list2.append(beta)
betas=np.array(data_list2)
print(betas)
df2=pd.DataFrame(betas,columns=['分布'])
print(df2.describe())
plt.hist(betas,100,density=True,color='red')
plt.ylim([0,100])
plt.show()
from scipy.stats import norm
domain=np.linspace(0,10,10000)
plt.plot(domain,norm.pdf(domain,df2.mean(),df2.std()))
plt.show()