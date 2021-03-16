# coding=utf-8
import numpy as np
import math
import scipy.stats as st

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

    def tree_e(self, S_0, X, sigma, delta, alpha, t, steps):  # European case
        u = np.exp(sigma * np.sqrt(t / steps))
        d = 1 / u  # 注意时间间隔为△t=t/steps
        P = (np.exp((self.r-delta) * t / steps) - d) / (u - d)
        prices = np.zeros(steps + 1)  # 生成最后一列的股票价格空数组
        c_values = np.zeros(steps + 1)  # 生成最后一列的期权价值空数组
        prices[0] = S_0 * d ** steps  # 最后一行最后一列的股票价格
        c_values[0] = np.maximum(np.minimum(prices[0] - X, alpha*prices[0]), 0)  # 最后一行最后一列的期权价值
        for i in range(1, steps + 1):
            prices[i] = prices[i - 1] * (u ** 2)  # 计算最后一列的股票价格
            c_values[i] = np.maximum(np.minimum(prices[i] - X, alpha*prices[i]), 0)  # 计算最后一列的期权价值
        for j in range(steps, 0, -1):  # 逐个节点往前计算
            for i in range(0, j):
                c_values[i] = (P * c_values[i + 1] + (1 - P) * c_values[i]) / np.exp(self.r * t / steps)
        return c_values[0]


    def tree_a(self, S_0, X, sigma, delta, alpha, t, steps):  # American case
        u=np.exp(sigma*np.sqrt(t/steps));d=1/u
        P=(np.exp((self.r-delta)*t/steps)-d)/(u-d)
        prices=np.zeros(steps+1)
        c_values=np.zeros(steps+1)
        prices[0]= S_0 * d ** steps
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

if __name__ == '__main__':
    S_0 = 100
    X = 80
    sigma = 0.171461
    delta = 0.017
    alpha = 0.5
    t = 1
    steps = 1000
    r = 0.0192

    S_incre = 1     # Stock price increment
    T_incre = 1/360  # Time increment

    T = Tree(r)

    P_1 = T.tree_e(S_0 + 2*S_incre, X, sigma, delta, alpha, t, steps)
    P_2 = T.tree_e(S_0 + S_incre, X, sigma, delta, alpha, t, steps)
    P_3 = T.tree_e(S_0, X, sigma, delta, alpha, t, steps)
    P_4 = T.tree_e(S_0 - S_incre, X, sigma, delta, alpha, t, steps)
    P_5 = T.tree_e(S_0 - 2*S_incre, X, sigma, delta, alpha, t, steps)

    P_l = T.tree_e(S_0, X, sigma, delta, alpha, t + T_incre, steps)   # Price with longer time.
    P_s = T.tree_e(S_0, X, sigma, delta, alpha, t - T_incre, steps)   # Price with shorter time.

    print('Tree Delta: ', (P_2 - P_4) / (2 * S_incre))
    print('Tree Gamma: ', ((P_1 - P_3) / (2 * S_incre)-(P_3 - P_5) / (2 * S_incre))/(2 * S_incre))
    print('Tree Theta: ', -(P_l - P_s) / (2 * T_incre))

    P_1 = pde(S_0 + 2 * S_incre, X, sigma, delta, alpha, t, r)
    P_2 = pde(S_0 + S_incre, X, sigma, delta, alpha, t, r)
    P_3 = pde(S_0, X, sigma, delta, alpha, t, r)
    P_4 = pde(S_0 - S_incre, X, sigma, delta, alpha, t, r)
    P_5 = pde(S_0 - 2 * S_incre, X, sigma, delta, alpha, t, r)

    P_l = pde(S_0, X, sigma, delta, alpha, t + T_incre, r)  # Price with longer time.
    P_s = pde(S_0, X, sigma, delta, alpha, t - T_incre, r)  # Price with shorter time.

    print('PDE Delta: ', (P_2 - P_4) / (2 * S_incre))
    print('PDE Gamma: ', ((P_1 - P_3) / (2 * S_incre) - (P_3 - P_5) / (2 * S_incre)) / (2 * S_incre))
    print('PDE Theta: ', -(P_l - P_s) / (2 * T_incre))

