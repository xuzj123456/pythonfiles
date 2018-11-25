# coding=utf-8
from macroeco.hw import *
c_bar = 1
def func(c_0, n=100):
    c = np.zeros((n, 1))
    k = np.zeros((n, 1))
    c[0] = c_0
    k[0] = k_0
    try:
        for i in range(n - 1):
            k[i + 1] = k[i] ** alpha + (1 - delta) * k[i] - c[i]
            c[i + 1] = (c[i] - c_bar) * beta * ((1 - delta) + alpha * k[i + 1] ** (alpha - 1)) + c_bar
            if k[i + 1] <= 0:
                raise Exception
        if abs(k[-1] - k_ss) <= 10 and abs(c[-1] - c_ss) <= 10:
            return k, c
    except:
        pass

a = func(1)