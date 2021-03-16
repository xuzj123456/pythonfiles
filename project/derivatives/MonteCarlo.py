# coding=utf-8
import numpy as np

def gen_paths(S_0, X, sigma_0, delta, alpha, T, steps, r, N): # N is the number of paths.
    dt = T/steps
    paths = np.zeros((steps+1, N), np.float64)
    paths[0] = S_0
    for t in range(1, steps + 1):
        rand = np.random.standard_normal(N)
        paths[t] = paths[t - 1] * np.exp((r -delta- 0.5 * sigma_0 ** 2) * dt + sigma_0 * np.sqrt(dt) * rand)
        paths[t] = [ max(p,0)   for p in paths[t]]
    return paths

def Europ(S_0, X, sigma_0, delta, alpha, T, steps, r, N):
    paths = gen_paths(S_0, X, sigma_0, delta, alpha, T, steps, r, N)
    prices = paths[-1]
    return [np.exp(-r*T)*np.maximum(np.minimum(prices[i] - X, alpha*prices[i]), 0) for i in range(len(prices)) ]

def America(S_0, X, sigma_0, delta, alpha, T, steps, r, N):
    paths = gen_paths(S_0, X, sigma_0, delta, alpha, T, steps, r, N)
    value = np.zeros_like(paths)
    value[-1]= np.exp(-r*T)*np.maximum(np.minimum(paths[-1] - X, alpha*paths[-1]), 0)
    for i in range(steps-1, -1, -1):
        e_value = np.maximum(np.minimum(paths[i] - X, alpha*paths[i]), 0)  # exercise value
        good_paths = value[i+1] != 0
        p = np.polyfit(paths[i][good_paths], np.exp(-r*(T/steps))*value[i+1][good_paths], 2)
        pp = np.poly1d(p)
        y = pp(paths[i][good_paths])
        h_value = np.zeros_like(e_value)
        h_value[good_paths]=y
        for j in range(N):
            value[i][j] = max(e_value[j], h_value[j])

    return value[0]

# Selcet laguerre polynomials as the basic function.
def America_L(S_0, X, sigma_0, delta, alpha, T, steps, r, N):
    paths = gen_paths(S_0, X, sigma_0, delta, alpha, T, steps, r, N)
    value = np.zeros_like(paths)
    value[-1]= np.exp(-r*T)*np.maximum(np.minimum(paths[-1] - X, alpha*paths[-1]), 0)
    for i in range(steps-1, -1, -1):
        e_value = np.maximum(np.minimum(paths[i] - X, alpha*paths[i]), 0)  # exercise value
        good_paths = value[i+1] != 0
        p = np.polynomial.laguerre.lagfit(paths[i][good_paths], np.exp(-r*(T/steps))*value[i+1][good_paths], 2)
        pp = np.poly1d(p)
        y = np.polynomial.laguerre.lagval(paths[i][good_paths], p)
        h_value = np.zeros_like(e_value)
        h_value[good_paths]=y
        for j in range(N):
            value[i][j] = max(e_value[j], h_value[j])

    return value[0]


if __name__ == '__main__':
    N = 10000
    S_0 = 100
    X = 80
    sigma_0 = 0.171461
    delta = 0.017
    alpha = 0.5
    T = 1
    steps = 1000
    r = 0.0192


    # print(np.mean(Europ(S_0, X, sigma_0, delta, alpha, T, steps, r, N)))

    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(10, 7))
    # plt.grid(True)
    # plt.xlabel('Steps')
    # plt.ylabel('Stok Price')
    # for i in range(30):
    #     plt.plot(S[:, i])

    # P = Europ(S_0, X, sigma_0, delta, alpha, T, steps, r, N)
    P=np.array([])
    for i in range(100):
        np.random.seed()
        P=np.append(P, np.mean(Europ(S_0, X, sigma_0, delta, alpha, T, steps, r, N)))

    print("95% confidence intervel:", np.percentile(P, 2.5), np.percentile(P, 97.5))


