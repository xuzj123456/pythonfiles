# coding=utf-8
import pandas as pd
import numpy as np
import os

# configuration
capital = 20000.0
fee = 5.0
size=1
option_value=0
remain_money=capital
total_money = [remain_money]
trade_option = pd.DataFrame()

# backtest settings


def get_vacation_dates():
    tt = []  # dates before vacation
    for i in range(1, len(t_list)):
        if t_list[i] - t_list[i-1] > pd.to_timedelta(4, unit='d'):
            tt.append(t_list[i])

    tt = pd.Series(tt)
    return tt

if __name__ == '__main__':
    f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
    etf_ivx = pd.read_excel(f_path, 'ivx')
    etf_hv30 = pd.read_excel(f_path, 'hv30')
    etf_close = pd.read_excel(f_path, "close")
    etf_last_date = pd.read_excel(f_path, "ETF_option_lasttradingdate")

    t_list = etf_ivx['date']
    vaca_dates = get_vacation_dates()

    for date in vaca_dates:
        dates = [ t_list[t_list.tolist().index(date)+i] for i in range(-2, 5) ]

