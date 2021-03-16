# coding=utf-8
import numpy as np

class Tree:
    def __init__(self, r):
        self.r = r

    def tree_europ(self, S, X, sigma, delta, alpha, t, steps):
        u = np.exp(sigma * np.sqrt(t / steps));
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


if __name__ == '__main__':
    T = Tree(0.0192)
    print(T.tree_america(100, 80, 0.171461, 0.017,0.5, 1, 1000))
    print(T.tree_europ(100, 80, 0.171461, 0.017, 0.5, 1, 1000))