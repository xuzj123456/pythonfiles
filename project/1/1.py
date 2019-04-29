# coding=utf-8
import pandas as pd
import os

f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
ivx_data = pd.read_excel(f_path, 'ivx')

t_list = ivx_data['date']
dt = t_list[1].timestamp()-t_list[0].timestamp()
tt = []     # dates before vacation
for i in range(1, len(t_list)):
    if t_list[i].timestamp()-t_list[i-1].timestamp() >= 4*dt:
        tt.append(t_list[i])

tt = pd.Series(tt)