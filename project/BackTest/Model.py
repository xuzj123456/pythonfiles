# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# configuration
fee_rate = 0.0003
slippage = 5.0
capital = 10000000
size=1
stop_profit_rate = 1
stop_loss_rate =  0.12

class BackTestModel:
    def __init__(self, daily_data_path_set, seasonal_data_path_set):
        self.daily_data = {}
        self.seasonal_data = {}
        self.stock = []
        for p in daily_data_path_set:
            self.daily_data[p.split('_')[1]] = pd.read_csv('./daily_data/' + p)
        for p in seasonal_data_path_set:
            self.seasonal_data[p.split('_')[2][:-4]] = pd.read_csv('./seasonal_data/' + p)
            self.stock.append(p.split('_')[1])
        self.day = self.daily_data['600000.SZ'].date.values
        self.remain_money = capital
        self.total_money = [self.remain_money]
        self.trade_stock = pd.DataFrame(columns=["date", "code", "size", 'price'])
        self.hold_stock = pd.DataFrame(columns=["date", "code", "size", 'price'])

    def Add_Open(self, date, num, stock_code, price):  # Open a position or add to a position.
        if self.daily_data[stock_code][self.day==date].isST.values[0] == 1:
            print("ST stock is not supported")
            return 0
        if self.daily_data[stock_code][self.day == date].tradestatus.values[0] == 0:
            print("The stock exchange is closed today.")
            return 0
        trade = pd.Series([date, stock_code, num, price], index=["date", "code", "size", 'price'])
        if  self.remain_money - ( price*num  + num*slippage + num * fee_rate ) >=0:
            self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
            if stock_code not in self.hold_stock.code:
                self.hold_stock = self.hold_stock.append(trade, ignore_index=True)
            else:
                i = self.hold_stock.code.index(stock_code)
                self.hold_stock.loc[i:i, 'price'] = (self.hold_stock[i].price*self.hold_stock[i]['size']+
                                                     num*price)/(num+self.hold_stock[i]['size'])
            self.remain_money -= (price * num + num * slippage + num * fee_rate)
        else:
            print("The principal is not sufficient.")
        print( "Date %s, buy %d shares of stock %s" % (date, num, stock_code))

    def Sell(self, date, num, stock_code, price): # Sell all shares or sell part of shares of a stock.
        if self.daily_data[stock_code][self.day == date].tradestatus.values[0] == 0:
            print("***Warning: The stock exchange is closed today, so the selling transaction failed.")
            return 0
        trade = pd.Series([date, stock_code, -num, price], index=["date", "code", "size", 'price'])
        self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
        if  num > self.hold_stock[stock_code == self.hold_stock.code]['size'][0]:
            print("No Sell-Short")
        else:
            self.hold_stock.loc[self.hold_stock['code'].values.tolist().index(stock_code)]['size'] -= num
            df = self.daily_data[stock_code]
            self.remain_money += price * num - num*slippage - num * fee_rate
            print("Date %s, sell %d shares of stock %s" % (date, num, stock_code))

    # If the return of a position exceeds 100%, then we will stop profit and close the position.
    def stop_profit(self, stock_code, date):
        buy_price = self.hold_stock[self.hold_stock['code']==stock_code].price[0][0]
        if self.daily_data[stock_code][self.day==date].high.values[0] >= buy_price*(1+stop_profit_rate):
            self.Sell(date, self.hold_stock[self.hold_stock['code']==stock_code]['size'][0], stock_code,
                      buy_price*(1+stop_profit_rate))
            print("Stop profit: all shares of stock %s has been selled out." % stock_code)

    # If the loss of a position exceeds -10%, then we will stop loss and close the position.
    def stop_loss(self, stock_code, date):
        buy_price = self.hold_stock[self.hold_stock['code'] == stock_code].price[0][0]
        if self.daily_data[stock_code][self.day==date].low.values[0] <= buy_price * (1 - stop_loss_rate):
            self.Sell(date, self.hold_stock[self.hold_stock['code'] == stock_code]['size'][0], stock_code,
                      buy_price * (1 + stop_profit_rate))
            print("Stop loss: all shares of stock %s has been selled out."% stock_code)

    # Test whether we should stop profit or stop loss, and recalculate the total assets we have at present every day.
    def Update(self, date):
        stock_value = 0
        for s in self.hold_stock.code:
            if self.daily_data[s][self.day == date].tradestatus.values[0] == 0:
                continue
            if self.hold_stock[self.hold_stock.code==s]['size'][0] != 0:
                self.stop_profit(s, date)
            if self.hold_stock[self.hold_stock.code==s]['size'][0] != 0:
                self.stop_loss(s, date)
            df = self.daily_data[s]
            stock_value += \
                float(df[date == df.date]['close']) * float(self.hold_stock[self.hold_stock.code == s]['size'])
        self.total_money.append(stock_value+self.remain_money)

    def Cacul_Performance(self):
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

        # Plot
        print('Return: %.2f%%' % (backtest_return * 100.0))
        print('Annualized Return: %.2f%%' % (annual_rtn * 100.0))
        print('Maximal Drawdown: %.2f%%' % (max_drawdown_ratio * 100.0))
        print('Annualized Vol: %.2f%%' % (100.0 * annual_vol))
        print('Sharpe Ratio: %.4f' % sharpe_ratio)
        print('Sortino Ratio: %.4f' % sortino_ratio)

        plt.figure(figsize=(8, 5))
        plt.plot(self.day, self.total_money[1:])
        plt.xticks([self.day[i] for i in range(0, len(self.day)-1, 80)], rotation = 20)
        plt.xlabel('Date')
        plt.ylabel('Money')
        plt.title('Money Curve')
        plt.grid(True)
        plt.show()


    def Run(self):
        for d in self.day:
            self.Strategy(d)
            self.Update(d)
            print(d)

        self.DAY_MAX = len(self.total_money) - 300

        self.Cacul_Performance()

    def select(self):
        self.selected_stock = []

    def Strategy(self, date):
        if date == '2014-01-20':
            i = np.argwhere(self.day==date)[0][0]
            self.Add_Open(date, 10000, '600000.SZ', self.daily_data['600183.SZ'][i:i+1].close.values)
        if date == '2015-06-30':
            i = np.argwhere(self.day == date)[0][0]
            self.Sell(date, 10000, '600000.SZ', self.daily_data['600183.SZ'][i:i+1].close.values)


if __name__ == '__main__':
    path_set_daily = os.listdir('./daily_data')
    path_set_seasonal = os.listdir('./seasonal_data')
    M = BackTestModel(path_set_daily, path_set_seasonal)
    M.Run()
