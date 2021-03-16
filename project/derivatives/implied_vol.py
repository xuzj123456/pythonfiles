# coding=utf-8
import math
import scipy.stats as st
import numpy as np

def pde(S_0, X, sigma, delta, alpha, t, r):
    d_1 = ((math.log(S_0, math.e) + (r - delta + sigma ** 2) * t) - math.log(X / (1 - alpha), math.e)) / (sigma * math.sqrt(t))
    d_2 = d_1 - math.log(1-alpha, math.e)/(sigma * math.sqrt(t))
    d_3 = d_1 - sigma * math.sqrt(t)
    d_4 = d_1 - sigma * math.sqrt(t) - math.log(1 - alpha, math.e) / (sigma * math.sqrt(t))
    result = (alpha-1) * S_0 * math.exp(-delta * t) * st.norm.cdf(d_1) + S_0 * math.exp(-delta * t) * st.norm.cdf(d_2) + \
             X * math.exp(-r) * st.norm.cdf(d_3) - X * math.exp(-r) * st.norm.cdf(d_4)
    return result

class Tree:
    def __init__(self, r):
        self.r = r

    def tree_europ(self, S, X, sigma, delta, alpha, t, steps):
        u = np.exp(sigma * np.sqrt(t / steps))
        d = 1 / u  # 注意时间间隔为△t=t/steps
        P = (np.exp((self.r-delta) * t / steps) - d) / (u - d)
        prices = np.zeros(steps + 1)  # 生成最后一列的股票价格空数组
        c_values = np.zeros(steps + 1)  # 生成最后一列的期权价值空数组
        prices[0] = S * d ** steps  # 最后一行最后一列的股票价格
        c_values[0] = np.maximum(np.minimum(prices[0] - X, alpha*prices[0]), 0)  # 最后一行最后一列的期权价值
        for i in range(1, steps + 1):
            prices[i] = prices[i - 1] * (u ** 2)  # 计算最后一列的股票价格
            c_values[i] = np.maximum(np.minimum(prices[i] - X, alpha*prices[i]), 0)  # 计算最后一列的期权价值
        for j in range(steps, 0, -1):  # 逐个节点往前计算
            for i in range(0, j):
                c_values[i] = (P * c_values[i + 1] + (1 - P) * c_values[i]) / np.exp(self.r * t / steps)
        return c_values[0]


    def tree_america(self, S, X, sigma, delta, alpha, t, steps):
        u=np.exp(sigma*np.sqrt(t/steps));d=1/u
        P=(np.exp((self.r-delta)*t/steps)-d)/(u-d)
        prices=np.zeros(steps+1)
        c_values=np.zeros(steps+1)
        prices[0]=S*d**steps
        c_values[0]=np.maximum(np.minimum(prices[0] - X, alpha*prices[0]), 0)
        for i in range(1,steps+1):
            prices[i]=prices[i-1]*(u**2)
            c_values[i]=np.maximum(np.minimum(prices[i] - X, alpha*prices[i]), 0)
        for j in range(steps,0,-1):
            for i in range(0,j):
                prices[i]=prices[i+1]*d#或者prices[i]=prices[i]*u
                c_values[i]=np.maximum((P*c_values[i+1]+(1-P)*c_values[i])/np.exp(self.r*t/steps),
                                       np.maximum(np.minimum(prices[i] - X, alpha * prices[i]), 0))#检查是否提前行权
        return c_values[0]

def implied_vol_pde(price, S_0, X, delta, alpha, T, r):  # Price parameter is the price of the derivative.
    h_bound = 1  # vol higher bound
    l_bound = 0   # vol lower bound
    vol = (h_bound + l_bound) / 2

    while h_bound-l_bound >= 0.00001:
        vol = (h_bound + l_bound) / 2
        p = pde(S_0, X, vol, delta, alpha, T, r)
        if p > price:
            h_bound = vol
        else:
            l_bound = vol

    return vol

def implied_vol_tree(func, price, S, X, delta, alpha, t, steps):
    h_bound = 1  # vol higher bound
    l_bound = 0  # vol lower bound
    vol = (h_bound + l_bound) / 2

    while h_bound-l_bound >= 0.00001:
        vol = (h_bound + l_bound) / 2
        p = func(S, X, vol, delta, alpha, t, steps)
        if p > price:
            h_bound = vol
        else:
            l_bound = vol

    return vol


if __name__ == '__main__':
    S_0 = 100
    X = 80
    sigma_0 = 0.171461
    delta = 0.017
    alpha = 0.5
    t = 1
    steps = 1000
    r = 0.0192

    print(implied_vol_pde(20.4807, S_0, X, delta, alpha, t, r))  # Do not import sigma parameter.
    T = Tree(r)
    print(implied_vol_tree(T.tree_europ, 20.599, S_0, X, delta, alpha, t, steps))
    print(implied_vol_tree(T.tree_america, 20.489, S_0, X, delta, alpha, t, steps))