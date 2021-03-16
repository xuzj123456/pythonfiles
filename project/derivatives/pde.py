# coding=utf-8
import math
import scipy.stats as st

def f(S_0, X, sigma_0, delta, alpha, T, r):
    d_1 = ((math.log(S_0, math.e)+(r-delta+sigma_0**2)*T)-math.log(X/(1-alpha), math.e))/(sigma_0*math.sqrt(T))
    d_2 = d_1 - math.log(1-alpha, math.e)/(sigma_0*math.sqrt(T))
    d_3 = d_1 - sigma_0*math.sqrt(T)
    d_4 = d_1 - sigma_0*math.sqrt(T) - math.log(1-alpha, math.e)/(sigma_0*math.sqrt(T))
    result = (alpha-1)*S_0*math.exp(-delta*T)*st.norm.cdf(d_1)+S_0*math.exp(-delta*T)*st.norm.cdf(d_2)+\
             X*math.exp(-r)*st.norm.cdf(d_3)-X*math.exp(-r)*st.norm.cdf(d_4)
    return result

if __name__ == '__main__':
    print(f(100, 80, 0.171461, 0.017, 0.5, 1, 0.0192))
