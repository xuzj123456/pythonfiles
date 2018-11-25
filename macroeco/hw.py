# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt


delta, alpha, beta = 0.05, 0.3, 0.95
k_ss = ((1/beta-1+delta)/alpha)**(1/(alpha-1))
k_0 = k_ss/2
k_max = (1/delta)**(1/(1-alpha))
k_G = (alpha/delta)**(1/(1-alpha))

def css(k):
    return k**alpha-delta*k
c_ss = css(k_ss)
c_max = css(k_G)

class Solution:
    @staticmethod
    def backward(n=200):
        c = np.zeros((n, 1))
        k = np.zeros((n, 1))
        c[n-1] = c_ss
        k[n-1] = k_ss-0.001     # 让C_t+1与C_t的比值略大于1
        for i in range(n-1, 0, -1):
            c[i-1] = c[i]/(beta*((1-delta)+alpha*k[i]**(alpha-1)))
            k[i-1] = (c[i-1]+k[i]+(alpha-1)*k_ss**alpha)/(alpha*k_ss**(alpha-1)+(1-delta))
            if k[i-1] <= k_0:
                c = c[i-1:]
                k = k[i-1:]     # 选取非零的有效期数
                break
        return k, c


    @staticmethod
    def forward(n=200):
        c_bar = 1
        for c_0 in np.linspace(c_bar, c_max, 10000):
            c = np.zeros((n, 1))
            k = np.zeros((n, 1))
            c[0] = c_0
            k[0] = k_0
            try:
                for i in range(n-1):
                    k[i+1] = k[i]**alpha+(1-delta)*k[i]-c[i]
                    c[i+1] = (c[i]-c_bar)*beta*((1-delta)+alpha*k[i+1]**(alpha-1))+c_bar
                    if k[i+1] <= 0:
                        raise Exception
                if abs(k[-1]-k_ss) <= 0.01 and abs(c[-1]-c_ss) <= 0.01:
                    return k, c
            except:
                pass
        return k, c


    @staticmethod
    def plot(k, c, title):
        fig, ax = plt.subplots()
        plt.xlim((0, k_max))
        plt.ylim((0, 1.5*c_max))
        k_simulation = np.linspace(0, k_max, 500)
        ax.plot(k_simulation, css(k_simulation), label ='$\dotk=0$', linestyle = '-.')
        plt.axvline(x = k_ss, ymin = 0, ymax = 1.5*c_max, label = '$\dotc=0$', linestyle = '-')
        plt.axvline(x = k_0, ymin = 0 ,ymax = 1.5*c_max, label = '$k_0$', linestyle = ':')
        ax.plot(k, c, label = "stable saddle path", linewidth = 2, linestyle = '--')
        ax.legend(loc = "upper right")
        ax.set_title(title, fontsize = 20, fontweight = 'heavy')
        plt.show()

if __name__ == '__main__':
    s = Solution
    k_back, c_back = s.backward()
    s.plot(k_back, c_back, 'Backward method')
    k_forward, c_forward = s.forward()
    s.plot(k_forward, c_forward, 'Forward method')
