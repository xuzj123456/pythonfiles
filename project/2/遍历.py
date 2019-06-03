# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from time import time
import os


# configuration
fee = 5.0
slippage = 5.0
capital = 20000.0
size=1

class S:
    def __init__(self):
        self.option_value = 0
        self.remain_money = capital
        self.total_money = [self.remain_money]
        self.trade_option = pd.DataFrame()


    def skew_ivx(self, date,at_name,out_name):
        if at_name in etf_ivx.columns and out_name in etf_ivx.columns:
            at_imvol = etf_ivx[etf_ivx.date == date][at_name].values[0].tolist()
            out_imvol = etf_ivx[etf_ivx.date == date][out_name].values[0].tolist()
            if at_imvol != 0:
                skeww = out_imvol / at_imvol
            else:
                skeww = "False"
        else:
            skeww = "False"
        return skeww

    def add_open(self, num,at_name,out_name):
        "正在开仓中的合约"
        if self.trade_option.empty:
            t = pd.Series([at_name, out_name, num], index=["at", "out", "size"])
            self.trade_option=self.trade_option.append(t, ignore_index=True)
        else:
            if at_name not in self.trade_option['at'].values:
                t = pd.Series([at_name, out_name, num], index=["at", "out", "size"])
                self.trade_option =self.trade_option.append(t, ignore_index=True)

    def Calendar_Spread(self, posit, date, at_name, out_name):  # 资金处理
        at_close = etf_close[etf_close.date == date][at_name].values[0].tolist()
        out_close = etf_close[etf_close.date == date][out_name].values[0].tolist()
        if posit == "buy":  # 买平值卖虚值
            num = size
            self.add_open(num, at_name, out_name)
#            print(str(date) + 'buy: '+str(at_name)+' and sell'+str(out_name))
            money_chg = -10000.0 * num * at_close + 15000.0 * num * out_close
        elif posit == "sell":  # 买虚值卖平值
            num = -size
            self.add_open(num, at_name, out_name)
#            print(str(date) + 'sell: '+str(at_name)+' and buy'+str(out_name))
            money_chg = 10000.0 * num * at_close - 15000.0 * num * out_close
        elif posit == "close buy":
            num = self.trade_option[self.trade_option['at'] == at_name]['size'].values[0].tolist()
            self.trade_option = self.trade_option[self.trade_option['at'] != at_name]
#            print(str(date) + 'close buy: '+str(at_name)+' and sell'+str(out_name))
            money_chg = 10000.0 * num * at_close - 15000.0 * num * out_close
        elif posit == "close sell":
            num = self.trade_option[self.trade_option['at'] == at_name]['size'].values[0].tolist()
            self.trade_option = self.trade_option[self.trade_option['at'] != at_name]
#            print(str(date) + 'close sell: ' + str(at_name) + ' and buy' + str(out_name))
            money_chg = -10000.0 * num * at_close + 15000.0 * num * out_close

        return money_chg - 2.5 * size * fee - 2.5 * size * slippage / 2.0

    def handle_ivx(self, date, _type, per1, per2, per3, per4):  # 下单信号； type=call/put
        at_name = etf_option_name[etf_option_name.date == date][self.a_name].values[0]
        out_name = etf_option_name[etf_option_name.date == date][self.o_name].values[0]

        # open position
        skew = self.skew_ivx(date, at_name, out_name)
        if at_name not in lastdate.symbol.values and _type == "call":
            at_name = at_name[:-4] + "%.2f" % (float(at_name[-4:]) + 0.05)
        elif at_name not in lastdate.symbol.values and _type == "put":
            at_name = at_name[:-4] + "%.2f" % (float(at_name[-4:]) - 0.05)
        expireday = lastdate[lastdate.symbol == at_name]['lasttradingdate'].values[0]
        expireday = pd.Timestamp(expireday)

        if self.befexp == "T" and (expireday - datetime.datetime.strptime(date, '%Y-%m-%d')).days < self.d:
            change = 0
        else:
            if self.trade_option.empty and skew != "False":
                if skew > per1:
                    posit = "buy"  # buy atm option,sell otm option
                    change = self.Calendar_Spread(posit, date, at_name, out_name)
                elif skew < per4:
                    posit = "sell"  # sell atm option,buy otm option
                    change = self.Calendar_Spread(posit, date, at_name, out_name)
                else:
                    change = 0
            else:
                change = 0

        # close position
        self.option_value = 0  # 持仓价值
        if self.trade_option.empty == False:
            for at_name in self.trade_option['at']:
                out_name = self.trade_option[self.trade_option['at'] == at_name]["out"].values[0]
                skew = self.skew_ivx(date, at_name, out_name)
                num = self.trade_option[self.trade_option['at'] == at_name]["size"].values.tolist()[0]
                at_close = etf_close[etf_close.date == date][at_name].values[0].tolist()
                out_close = etf_close[etf_close.date == date][out_name].values[0].tolist()
                if num > 0 and ((skew != "False" and skew < per2) or self.expire(at_name, date) == "T"):
                    posit = "close buy"
                    change = self.Calendar_Spread(posit, date, at_name, out_name)
                elif num < 0 and ((skew != "False" and skew > per3) or self.expire(at_name, date) == "T"):
                    posit = "close sell"
                    change = self.Calendar_Spread(posit, date, at_name, out_name)
                else:
                    self.option_value += 10000.0 * num * at_close - 15000.0 * num * out_close
                    change = 0
        else:
            change = 0

        self.remain_money += change
        self.total_money.append(self.remain_money + self.option_value)

    def expire(self, at_name, date):
        if np.datetime64(date) in lastdate.lasttradingdate.values and (
                at_name in lastdate[lastdate.lasttradingdate == date]['symbol'].values):
            expireTF = "T"
        else:
            expireTF = "F"
        return expireTF

    def cacul_performance(self):
        """
        Calculate annualized return, Sharpe ratio, maximal drawdown, return volatility and sortino ratio
        :return: annualized return, Sharpe ratio, maximal drawdown, return volatility and sortino ratio
        """

        rtn = self.total_money[-1] / capital - 1

        annual_rtn = np.power(rtn + 1, 252.0 / self.DAY_MAX) - 1  # 复利
        annual_rtn = rtn * 252 / self.DAY_MAX  # 单利
#        print(self.total_money)
        annual_lst = [(self.total_money[k + 301] - self.total_money[k + 300]) / self.total_money[k + 300] for k in
                      range(self.DAY_MAX - 1)]
        annual_vol = np.array(annual_lst).std() * np.sqrt(252.0)

        rf = 0.04
        semi_down_list = [annual_lst[k] for k in range(self.DAY_MAX - 1) if annual_lst[k] < rf]
        semi_down_vol = np.array(semi_down_list).std()
        sharpe_ratio = (annual_rtn - rf) / annual_vol
        sortino_ratio = (annual_rtn - rf) / semi_down_vol

        max_drawdown_ratio = 0
        for e, i in enumerate(self.total_money):
            for f, j in enumerate(self.total_money):
                if f > e and float(j - i) / i < max_drawdown_ratio:
                    max_drawdown_ratio = float(j - i) / i

        backtest_return = self.total_money[-1] / capital - 1

        print("boundary %d %d %d %d" % (self.up_buy, self.down_close_buy, self.up_close_sell, self.down_sell))
        print("option_type", self.option_type_1, "type", self.option_type_2)
        print(self.befexp, "before expire %d don't trade " % (self.d))
        ## 回测绩效与绘图
        print('Return: %.2f%%' % (backtest_return * 100.0))
        print('Annualized Return: %.2f%%' % (annual_rtn * 100.0))
        print('Maximal Drawdown: %.2f%%' % (max_drawdown_ratio * 100.0))
        print('Annualized Vol: %.2f%%' % (100.0 * annual_vol))
        print('Sharpe Ratio: %.4f' % sharpe_ratio)
        print('Sortino Ratio: %.4f' % sortino_ratio)

        plt.figure(figsize=(8, 5))
        plt.plot(self.day, self.total_money[1:])
        plt.xlabel('Date')
        plt.ylabel('Money')
        plt.title('Money Curve')
        plt.grid(True)
        plt.show()

    def run(self):
        if self.option_type_1 == "out" and self.option_type_2 == "call":
            self.a_name, self.o_name = 'out_call', 'out2_call'
        elif self.option_type_1 == "out" and self.option_type_2 == "put":
            self.a_name, self.o_name = 'out_put', 'out2_put'
        elif self.option_type_1 == "at" and self.option_type_2 == "call":
            self.a_name, self.o_name = 'call', 'out_call'
        elif self.option_type_1 == "at" and self.option_type_2 == "put":
            self.a_name, self.o_name = 'put', 'out_put'
        else:
            print("_type error")


        a = []
        for date in etf_option_name.date.values:  # date为datetime
            date = pd.to_datetime(str(date)).strftime('%Y-%m-%d')
            at_name = etf_option_name[etf_option_name.date == date][self.a_name].values[0]
            out_name = etf_option_name[etf_option_name.date == date][self.o_name].values[0]
            if at_name in etf_ivx.columns and out_name in etf_ivx.columns:
                at_imvol = etf_ivx[etf_ivx.date == date][at_name].values[0].tolist()
                out_imvol = etf_ivx[etf_ivx.date == date][out_name].values[0].tolist()
                if at_imvol != 0:
                    skeww = out_imvol / at_imvol
                    a.append(skeww)
                else:
                    skeww = 0
        a = [x for x in a if np.isnan(x) == False and x != 0]

        self.day = []
        for i, date in enumerate(etf_option_name.date.values):  # date为datetime
            date = pd.to_datetime(str(date)).strftime('%Y-%m-%d')  # date为字符串
            if i < 300:
                per1, per2, per3, per4 = 100, 0, 0, -1
            else:
                (per1, per2, per3, per4) = (
                    np.percentile(a[0:i], self.up_buy), np.percentile(a[0:i], self.down_close_buy),
                    np.percentile(a[0:i], self.up_close_sell),
                    np.percentile(a[0:i], self.down_sell))
            self.handle_ivx(date, self.option_type_2, per1, per2, per3, per4)
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            self.day.append(date)

        self.DAY_MAX = len(self.total_money) - 300

#        self.cacul_performance()

if __name__ == '__main__':
    start = time()

    f_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '50etf2018_9_20.xlsx')
    etf_close = pd.read_excel(f_path, "close")
    etf_ivx = pd.read_excel(f_path, "ivx")
    lastdate = pd.read_excel(f_path, "ETF_option_lasttradingdate")
    etf_option_name = pd.read_excel(f_path, "at_money_name")

    # s = S()
    #
    # (s.up_buy, s.down_close_buy, s.up_close_sell, s.down_sell) = (75, 65, 35, 25)  # 上下界
    #
    # s.option_type_1 = "out"  # at/out，at为平值期权和虚值1期权，out为虚值1与虚值2期权
    # s.option_type_2 = "put"  # call/put，进行操作的期权
    # s.befexp = "T"  # 是否在到期日前d天内不交易
    # s.d = 7
    #
    # s.run()

    max_total=[0]
    s=S()
    for i1 in range(60, 100, 5):
        for i2 in range(55, i1, 5):
            for i4 in range(5, 45, 5):
                for i3 in range(i4+5, 50, 5):
                    for i5 in ['at']:
                        for i6 in ['call']:
                            s.__init__()
                            s.befexp = "T"
                            s.d = 7

                            (s.up_buy, s.down_close_buy, s.up_close_sell, s.down_sell) = (i1, i2, i3, i4)
                            s.option_type_1 = i5
                            s.option_type_2 = i6
                            s.run()
                            if s.total_money[-1] >= max_total[-1]:
                                max_total = s.total_money
                                config = [i1, i2, i3, i4, i5, i6]

    print(max_total)
    print(config)

    end = time()
    print('total time is %.6f seconds' % (end - start))