# coding=utf-8
# 在大于等于4天的节假日前后根据隐含波动率变化制定的交易策略
import pandas as pd
import numpy as np
import os

# configuration
capital = 20000.0
fee = 5.0
slippage = 5.0
size = 1
remain_money = capital
total_money = [remain_money]
trade_option = pd.DataFrame()


def get_vacation_dates():
    tt = []  # dates before vacation
    for i in range(1, len(t_list)):
        if t_list[i] - t_list[i-1] > pd.to_timedelta(4, unit='d'):
            tt.append(t_list[i])

    tt = pd.Series(tt)
    return tt

def add_open(num, call_name, put_name):
    global trade_option
    # 正在开仓中的合约
    if trade_option.empty:
        t = pd.Series([call_name,put_name,num], index=["call","put","size"])
        trade_option = trade_option.append(t, ignore_index=True)
    else:
        if call_name not in trade_option['call'].values:
            t = pd.Series([call_name,put_name,num], index=["call","put","size"])
            trade_option = trade_option.append(t, ignore_index=True)
    return trade_option

def straddle(date, posit, call_name, put_name):#资金处理
    global trade_option
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
    global total_money, remain_money, trade_option
    option_value = 0
    # 节前第一个交易日买入跨式
    call_name = etf_option_name[etf_option_name.date == dates[1]]['call'].values[0]
    put_name = etf_option_name[etf_option_name.date == dates[1]]['put'].values[0]

    call_ivx = etf_ivx[etf_ivx.date == dates[1]][call_name].values[0]
    put_ivx = etf_ivx[etf_ivx.date == dates[1]][put_name].values[0]
    ivx = (call_ivx + put_ivx) / 2

    if etf_hv30[etf_hv30.date == dates[1]]['hv'].values[0] >= ivx:    # 之后可以替换条件
        call_close = etf_close[etf_close.date == dates[1]][call_name].values[0]
        put_close = etf_close[etf_close.date == dates[1]][put_name].values[0]
        posit = 'buy'
        change = straddle(dates[1], posit, call_name, put_name)
        option_value = option_value + 10000.0 * size * call_close + 10000.0 * size * put_close
        remain_money += change
        total_money.append(remain_money + option_value)

        #节后第一个交易日平仓
        call_close = etf_close[etf_close.date == dates[2]][call_name].values[0]
        put_close = etf_close[etf_close.date == dates[2]][put_name].values[0]
        posit = 'close buy'
        change = straddle(dates[2], posit, call_name, put_name)
        remain_money += change
        total_money.append(remain_money)

        trading_time.append(2)
        daily_rtn.append((total_money[-1]-total_money[-2])/total_money[-2])


    option_value = 0
    # 节后第一个交易日卖出跨式
    call_name = etf_option_name[etf_option_name.date == dates[2]]['call'].values[0]
    put_name = etf_option_name[etf_option_name.date == dates[2]]['put'].values[0]
    call_ivx = etf_ivx[etf_ivx.date == dates[2]][call_name].values[0]
    put_ivx = etf_ivx[etf_ivx.date == dates[2]][put_name].values[0]
    ivx = (call_ivx + put_ivx) / 2

    if etf_hv30[etf_hv30.date == dates[2]]['hv'].values[0] <= ivx:
        call_close = etf_close[etf_close.date == dates[2]][call_name].values[0]
        put_close = etf_close[etf_close.date == dates[2]][put_name].values[0]
        posit = 'sell'
        change = straddle(dates[2], posit, call_name, put_name)
        option_value = option_value - 10000.0 * size * call_close - 10000.0 * size * put_close
        remain_money += change
        total_money.append(remain_money + option_value)

        #节后第五个交易日平仓
        call_close = etf_close[etf_close.date == dates[6]][call_name].values[0]
        put_close = etf_close[etf_close.date == dates[6]][put_name].values[0]
        posit = 'close sell'
        change = straddle(dates[6], posit, call_name, put_name)
        remain_money += change
        total_money.append(remain_money)

        trading_time.append(5)
        daily_rtn.append((total_money[-1] - total_money[-2]) / (total_money[-2]*4))

def performance():
    backtest_rtn = total_money[-1] / capital - 1

    DAY_len = sum(trading_time)
    annual_rtn = backtest_rtn * 252 / DAY_len

    annual_vol = np.array(daily_rtn).std() * np.sqrt(252.0)
    rf = 0.04
    sharpe_ratio = (annual_rtn - rf) / annual_vol

    max_drawdown_ratio = 0
    for e, i in enumerate(total_money):
        for f, j in enumerate(total_money):
            if f > e and float(j - i) / i < max_drawdown_ratio:
                max_drawdown_ratio = float(j - i) / i

    print('Return: %.2f%%' % (backtest_rtn * 100.0))
    print('Annualized Return: %.2f%%' % (annual_rtn * 100.0))
    print('Annualized Vol: %.2f%%' % (annual_vol * 100.0))
    print('Sharpe Ratio: %.4f' % sharpe_ratio)
    print('Maximal Drawdown: %.2f%%' % (max_drawdown_ratio * 100.0))


if __name__ == '__main__':
    f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
    etf_ivx = pd.read_excel(f_path, 'ivx')
    etf_hv30 = pd.read_excel(f_path, 'hv30')
    etf_close = pd.read_excel(f_path, "close")
    etf_option_name = pd.read_excel(f_path, "at_money_name")

    t_list = etf_ivx['date']
    vaca_dates = get_vacation_dates()

    trading_time = []       # list，每次持仓时间
    daily_rtn = []

    for date in vaca_dates:
        dates = [ t_list[t_list.tolist().index(date)+i] for i in range(-2, 5) ]     # 节假日前两个与后五个交易日
        handle(dates)

    performance()
