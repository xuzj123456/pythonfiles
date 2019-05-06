# coding=utf-8
import pandas as pd
import os


if __name__ == '__main__':
    f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
    etf_ivx = pd.read_excel(f_path, 'ivx')
    etf_hv30 = pd.read_excel(f_path, 'hv30')
    etf_close = pd.read_excel(f_path, "close")
    etf_last_date = pd.read_excel(f_path, "ETF_option_lasttradingdate")

