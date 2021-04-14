# coding=utf-8
import pandas as pd
import numpy as np

Apple = pd.read_csv('AAPL.csv')
Aetna = pd.read_csv('AET.csv')
AEP = pd.read_csv('AEP.csv')
GS = pd.read_csv('GS.csv')
T = pd.read_csv('T.csv')
LIBOR = pd.read_excel('USD1MTD156N.xlsx')

r_f = np.array(LIBOR.USD1MTD156N.values[:-1])

Apple_price = np.array(Apple['Adj Close'])
r_apple = np.array([ Apple_price[i+1]/Apple_price[i]-1 for i in range(len(Apple_price)-1) ])
exr_apple = r_apple - r_f  # Excess return

Aetna_price = np.array(Aetna['Adj Close'])
r_Aetna = np.array([ Aetna_price[i+1]/Aetna_price[i]-1 for i in range(len(Aetna_price)-1) ])
exr_Aetna = r_Aetna - r_f

AEP_price = np.array(AEP['Adj Close'])
r_AEP = np.array([ AEP_price[i+1]/AEP_price[i]-1 for i in range(len(AEP_price)-1) ])
exr_AEP = r_AEP - r_f

GS_price = np.array(GS['Adj Close'])
r_GS = np.array([ GS_price[i+1]/GS_price[i]-1 for i in range(len(GS_price)-1) ])
exr_GS = r_GS - r_f

T_price = np.array(T['Adj Close'])
r_T = np.array([ T_price[i+1]/T_price[i]-1 for i in range(len(T_price)-1) ])
exr_T = r_T - r_f

t = 10*12-1
N = 5
lamb = 1/4

# Excess return
exr = pd.DataFrame([exr_apple, exr_Aetna, exr_AEP, exr_GS, exr_T], index=['Apple', 'Aetna', 'AEP', 'GS', 'T']).transpose()
exr_insam = exr[:60]
exr_ousam = exr[60:]
# All return
allr = pd.DataFrame([exr_apple, exr_Aetna, exr_AEP, exr_GS, exr_T, r_f], index=['Apple', 'Aetna', 'AEP', 'GS', 'T', 'risk_free_rate']).transpose()
allr_insam = exr[:60]
allr_ousam = exr[60:]

# Unbiased and MLE
cov_insam = exr_insam.cov()
cov_mle = cov_insam*(t-1)/t
mean_insam = exr_insam.mean()

x = np.matmul(np.linalg.pinv(cov_mle), mean_insam)
w_mle = lamb*x
w0_mle = 1-sum(w_mle)
w_unbias = w_mle * (t-N-2)/t
w0_unbias = 1-sum(w_unbias)

