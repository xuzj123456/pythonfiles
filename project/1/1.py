# coding=utf-8
import pandas as pd
import numpy as np
import os

# configuration
capital = 20000.0
fee = 5.0
slippage = 5.0
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

def add_open(num,call_name,put_name):
    "正在开仓中的合约"
    if trade_option.empty:
        t = pd.Series([call_name,put_name,num], index=["call","put","size"])
        trade_option = trade_option.append(t, ignore_index=True)
    else:
        if call_name not in trade_option['call'].values:
            t = pd.Series([call_name,put_name,num], index=["call","put","size"])
            trade_option = trade_option.append(t, ignore_index=True)
    return trade_option

def straddle(date,posit,call_name,put_name):#资金处理
    call_close = etf_close[etf_close.date==date][call_name].values[0]
    put_close = etf_close[etf_close.date==date][put_name].values[0]

    if posit=="buy": #买跨式期权
        num=size
        add_open(num,call_name,put_name)
        print(str(date) + 'buy: '+str(call_name)+' and '+str(put_name))
        money_chg=-10000.0*size*call_close-10000.0*size*put_close
    elif posit=="sell":#卖跨式期权
        num=-size
        add_open(num,call_name,put_name)
        print(str(date) + 'sell: '+str(call_name)+' and '+str(put_name))
        money_chg=10000.0*size*call_close+10000.0*size*put_close
    elif posit=="close buy":
        trade_option=trade_option[trade_option['call']!=call_name]
        print(str(date) + 'close buy: sell '+str(call_name)+' and '+str(put_name))
        money_chg=10000.0*size*call_close+10000.0*size*put_close
    elif posit=="close sell":
        trade_option=trade_option[trade_option['call']!=call_name]
        print(str(date) + 'close sell: buy '+str(call_name)+' and '+str(put_name))
        money_chg=-10000.0*size*call_close-10000.0*size*put_close

    return money_chg - 2 * size * fee - 2 * size * slippage / 2.0

def handle(dates):
    pass



if __name__ == '__main__':
    f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
    etf_ivx = pd.read_excel(f_path, 'ivx')
    etf_hv30 = pd.read_excel(f_path, 'hv30')
    etf_close = pd.read_excel(f_path, "close")
    etf_last_date = pd.read_excel(f_path, "ETF_option_lasttradingdate")

    t_list = etf_ivx['date']
    vaca_dates = get_vacation_dates()

    for date in vaca_dates:
        dates = [ t_list[t_list.tolist().index(date)+i] for i in range(-2, 5) ]     # 节假日前两个与后五个交易日
        handle(dates)
