# coding=utf-8
import numpy as np


T = 1000

mu = 2
phi_1 = 0.7
theta_1 = 0.1

alpha_0 = 0.3
alpha_1 = 0.05
beta_1 = 0.9

r = np.empty(T+1)
a = np.empty(T+1)
sigma = np.empty(T+1)
r[0], a[0], sigma[0] = 2, 0, 0.4

e = np.random.normal(0, 1, T+1)

for t in range(1, T+1):
    sigma[t] = (alpha_0 + alpha_1*a[t-1]**2 + beta_1*sigma[t-1]**2)**0.5
    a[t] = e[t] * sigma[t]
    r[t] = mu + phi_1*(r[t-1]-mu) - theta_1*a[t-1] + a[t]

