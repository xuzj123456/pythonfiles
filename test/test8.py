# coding=utf-8
import  matplotlib.pyplot as plt
import numpy as np

X = np.linspace(0,70, 10000)
Y1 = [-2 if x <= 50 else x-52 for x in X]
Y2 = [-3 if x >=45 else 42-x for x in X]
Y3 = np.array(Y1)+np.array(Y2)

plt.plot(X,Y1, label='call option')
plt.plot(X,Y2, label='put option')
plt.plot(X,Y3, label='portfolio')
plt.legend()