# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import os


# configuration
class Data_obtain(object):
    def __init__(self, path, start='20100101', end='20200101'):
        self.start = start
        self.end = end
        self.daily_data = {}
        self.fin_data = {}
        self.Factor_matrix = {}
        self.statDate = []
        self.obtain_data(path)

    def obtain_data(self, path):
        self.Accessible = set([i[9:15] + '.SH' if i[6:8] == "sh" else i[9:15] + '.SZ'
                               for i in
                               os.listdir('./All_stocks_trade')])
        # 交易数据
        daily_data_path_set = os.listdir(path)
        for p in daily_data_path_set:
            self.daily_data[p.split('.')[1] + '.' + p[6:8].upper()] = pd.read_csv(path + '/' + p,
                                                                                  parse_dates=['date'],
                                                                                  index_col='date')

        # 确定财报发布日
        self.TradDay = pd.read_csv("./数据/交易日期.csv", index_col='交易日期', parse_dates=['交易日期'])
        self.statDate = [[str(self.TradDay.resample('M').last()['{}-{}'.format(i, j)]['Tradingdate'].values[0])
                          for j in [4, 8, 10]] for i in range(int(self.start[:4]), int(self.end[:4]) + 1)]
        self.statDate = [int(a) for j in self.statDate for a in j if
                         int(a) >= int(self.start) and int(a) <= int(self.end) + 1]

        #         self.base_index800 = pd.read_excel("./数据/基准指数.xlsx", index_col='日期').loc[self.start:self.end, ]  # 基准指数
        self.reference = pd.read_csv("./数据/history_Index_data.csv", index_col='上证指数', parse_dates=['上证指数'])

        # 金融数据
        self.can_trade = {}
        for i in self.statDate:
            self.can_trade[i] = pd.read_csv("./数据/交易状态/{}.csv".format(i))['可交易股票']
            temp_df = pd.read_csv("./数据/Financial_Data/{}.csv".format(i))
            self.fin_data[i] = temp_df[temp_df['WIND_CODE'].isin(self.can_trade[i])].set_index('WIND_CODE')
            cir_mark_val = pd.read_excel("./数据/流通市值/{}.xlsx".format(i), index_col="Unnamed: 0").set_index('WIND代码')
            self.fin_data[i] = self.fin_data[i].join(cir_mark_val, how="left")  # "当日流通市值"
            self.fin_data[i]['Code'] = self.fin_data[i].index
        # 因子矩阵

        self.Factor_matrix['ROE连续两期增长'] = pd.read_excel("./数据/ROE5年标准差.xlsx", sheet_name='ROE连续两期增长',
                                                        index_col='证券代码')
        self.Factor_matrix['ROE连续三期增长'] = pd.read_excel("./数据/ROE5年标准差.xlsx", sheet_name='ROE连续三期增长',
                                                        index_col='证券代码')
        self.Factor_matrix['ROE连续四期增长'] = pd.read_excel("./数据/ROE5年标准差.xlsx", sheet_name='ROE连续四期增长',
                                                        index_col='证券代码')
        self.Factor_matrix['ROE波动'] = pd.read_excel("./数据/ROE5年标准差.xlsx", sheet_name='5年标准差', index_col='证券代码')

        self.Factor_matrix['毛利润连续两期增长'] = pd.read_excel("./数据/毛利率连续增长.xlsx", sheet_name='连续两期增长', index_col='证券代码')
        self.Factor_matrix['净利润增长率'] = pd.read_excel("./数据/净利润增长率.xlsx", index_col='证券代码')

        self.Factor_matrix['单毛利率连续增长'] = pd.read_excel("./数据/单毛利率连续增长.xlsx", sheet_name='连续两期增长', index_col='证券代码')
        self.Factor_matrix['单季度净利润同比增长率增长'] = pd.read_excel("./数据/单季度净利润增长.xlsx", sheet_name='连续两期增长',
                                                            index_col='证券代码')

        self.Factor_matrix['PE_TTM'] = pd.read_excel("./数据/历史估值水平.xlsx", sheet_name='pettm', index_col='证券代码')
        self.Factor_matrix['PB_MQR'] = pd.read_excel("./数据/历史估值水平.xlsx", sheet_name='pbmqr', index_col='证券代码')
        self.Factor_matrix['PE历史分位'] = pd.read_excel("./数据/历史估值水平.xlsx", sheet_name='pe历史分位', index_col='证券代码')
        self.Factor_matrix['PE历史分位'] = self.Factor_matrix['PE历史分位'].drop(['一级行业', '二级行业'], axis=1)
        self.Factor_matrix['PB历史分位'] = pd.read_excel("./数据/历史估值水平.xlsx", sheet_name='pb历史分位', index_col='证券代码')

        # 筛选数据预处理，波动率低的80%
        self.Factor_matrix['ROE波动'] = self.Factor_matrix['ROE波动'] < [
            np.percentile(self.Factor_matrix['ROE波动'][i].dropna(), 80, axis=0)
            for i in self.Factor_matrix['ROE波动'].columns]

        # 要ROE要大于10%

        self.Factor_matrix['ROE连续两期增长'] = self.Factor_matrix['ROE连续两期增长'] == 1
        self.Factor_matrix['毛利润连续两期增长'] = self.Factor_matrix['毛利润连续两期增长'] == 1
        self.Factor_matrix['净利润增长率'] = self.Factor_matrix['净利润增长率'] > 10
        self.Factor_matrix['PE历史分位'] = self.Factor_matrix['PE历史分位'] < [
            np.percentile(self.Factor_matrix['PE历史分位'][i].dropna(), 60, axis=0)
            for i in self.Factor_matrix['PE历史分位'].columns]
        self.Index = pd.read_excel('./数据/指数行情序列.xlsx', dtype={'时间': 'str'}).dropna()
        self.Index['时间'] = self.Index['时间'].apply(lambda x: x[:4] + x[5:7] + x[8:10])
        self.Index['One oreder'] = (self.Index['万得全A'].shift(-1) - self.Index['万得全A'])
        self.Index['PE increase rate'] = self.Index['One oreder'] / self.Index['万得全A']


class BackTestModel():
    def __init__(self, Data_obtain):
        self.start = Data_obtain.start
        self.end = Data_obtain.end
        self.Y_start = int(self.start[:4])
        self.Y_end = int(self.end[:4])
        self.parameters()
        self.daily_data = Data_obtain.daily_data
        self.fin_data = Data_obtain.fin_data
        self.Factor_matrix = copy.deepcopy(Data_obtain.Factor_matrix)
        self.statDate = Data_obtain.statDate
        self.Index = Data_obtain.Index
        self.Accessible = Data_obtain.Accessible
        self.can_trade = Data_obtain.can_trade
        #         self.base_index800 = Data_obtain.base_index800
        self.reference = Data_obtain.reference

        # self.Financial_df = np.read('./Financial_data')
        self.day = np.array(Data.TradDay.loc[self.start:self.end, 'Tradingdate'])
        self.trade_stock = pd.DataFrame(columns=["date", "code", "size", 'price', 'return rate'])
        self.hold_stock = pd.DataFrame(columns=["date", "code", "size", 'price'])

    def parameters(self, fee_rate=0.003, slippage=0.02, capital=10000000, size=1, stop_profit_rate=1,
                   stop_loss_rate=0.12):
        self.fee_rate = fee_rate
        self.slippage = slippage
        self.capital = capital
        self.size = size
        self.stop_profit_rate = stop_profit_rate
        self.stop_loss_rate = stop_loss_rate
        self.remain_money = self.capital
        self.total_money = [self.remain_money]



    def Add_Open(self, date, num, stock_code, price):  # Open a position or add to a position.
        if self.daily_data[stock_code][self.daily_data[stock_code].index == str(date)].isST.values[0] == 1:
            print("ST stock is not supported")
            return 0
        if self.daily_data[stock_code][self.daily_data[stock_code].index == str(date)].tradestatus.values[0] == 0:
            print("The stock exchange is closed today.")
            return 0
        trade = pd.Series([date, stock_code, num, price + self.slippage + price * self.fee_rate],
                          index=["date", "code", "size", 'price'])
        # 交易，首先判断是否在持仓中，不在考虑是否能够直接购买。在的话需要减去已有仓位，进行加仓或者减仓
        if stock_code not in self.hold_stock.code.tolist():
            if self.remain_money - (price * num + num * self.slippage + num * price * self.fee_rate) >= 0:
                self.hold_stock = self.hold_stock.append(trade, ignore_index=True)
                self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
                self.remain_money -= (price * num + num * price * self.fee_rate + num * self.fee_rate)
            else:
                print("The principal is not sufficient.")
        else:
            i = self.hold_stock[self.hold_stock['code'] == stock_code].index
            L_num = self.hold_stock.loc[i, 'size'].values[0]
            if L_num > num:
                self.Sell(date, num, stock_code, price)
                print("Have obtained enough shares and sold {} shares stocks".format(L_num - num))
            else:
                num = num - L_num
                trade = pd.Series([date, stock_code, num, price + self.slippage + price * self.fee_rate],
                                  index=["date", "code", "size", 'price'])
                if self.remain_money - (price * num + num * self.slippage + num * price * self.fee_rate) >= 0:
                    self.hold_stock.loc[i, 'size'] = num + L_num
                    self.hold_stock.loc[i, 'price'] = (self.hold_stock.loc[i, 'price'].values[0] * L_num +
                                                       (
                                                               price * num + num * price * self.fee_rate + num * self.fee_rate)) / (
                                                              num + L_num)
                    self.remain_money -= (price * num + num * self.slippage + num * price * self.fee_rate)
                    self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
                else:
                    print("The principal is not sufficient.")

    def Sell(self, date, num, stock_code, price):  # Sell all shares or sell part of shares of a stock.
        if self.daily_data[stock_code][self.daily_data[stock_code].index == str(date)].tradestatus.values[0] == 0:
            print("***Warning: The stock exchange is closed today, so the selling transaction failed.")
            return 0
        # 买入考虑手续费，卖出不考虑
        if num < 0:
            print("No Sell-Short, have sell all the stock")
        else:
            if num == 0:
                L_num = \
                self.hold_stock.loc[self.hold_stock[self.hold_stock['code'] == stock_code].index, "size"].values[0]
                L_price = self.hold_stock.loc[self.hold_stock[self.hold_stock['code'] == stock_code].index, "price"]
                trade = pd.Series([date, stock_code, -L_num, (price - self.slippage),
                                   (((price - self.slippage) - L_price) / L_price).values[0]],
                                  index=["date", "code", "size", 'price', 'return rate'])
                self.hold_stock = self.hold_stock.drop(self.hold_stock[self.hold_stock['code'] == stock_code].index)
                self.remain_money += price * (L_num) - (L_num) * self.slippage
                self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
                print("Date %s, sell %d shares of stock %s" % (date, L_num, stock_code))
            else:
                L_num = \
                self.hold_stock.loc[self.hold_stock[self.hold_stock['code'] == stock_code].index, "size"].values[0]
                L_price = self.hold_stock.loc[self.hold_stock[self.hold_stock['code'] == stock_code].index, "price"]
                trade = pd.Series([date, stock_code, -L_num + num, (price - self.slippage),
                                   (((price - self.slippage) - L_price) / L_price).values[0]],
                                  index=["date", "code", "size", 'price', 'return rate'])
                self.hold_stock.loc[self.hold_stock[self.hold_stock['code'] == stock_code].index, "size"] = num
                self.remain_money += price * (L_num - num) - (L_num - num) * self.slippage
                self.trade_stock = self.trade_stock.append(trade, ignore_index=True)
                print("Date %s, sell %d shares of stock %s" % (date, L_num - num, stock_code))

    # If the return of a position exceeds 100%, then we will stop profit and close the position.
    def stop_profit(self, stock_code, date):
        buy_price = self.hold_stock[self.hold_stock['code'] == stock_code].price.values[0]
        if self.daily_data[stock_code][self.daily_data[stock_code].index == str(date)].high.values[0] >= buy_price * (
                1 + self.stop_profit_rate):
            self.Sell(date, 0, stock_code,
                      buy_price * (1 + self.stop_profit_rate))
            print("Stop profit: all shares of stock %s has been selled out." % stock_code)

    # If the loss of a position exceeds -10%, then we will stop loss and close the position.
    def stop_loss(self, stock_code, date):
        buy_price = self.hold_stock[self.hold_stock['code'] == stock_code].price.values[0]
        if self.daily_data[stock_code][self.daily_data[stock_code].index == str(date)].low.values[0] <= buy_price * (
                1 - self.stop_loss_rate):
            self.Sell(date, 0, stock_code,
                      buy_price * (1 - self.stop_loss_rate))
            print("Stop loss: all shares of stock %s has been selled out." % stock_code)

    # Test whether we should stop profit or stop loss, and recalculate the total assets we have at present every day.
    def Update(self, date):
        stock_value = 0
        for s in self.hold_stock.code:
            if self.daily_data[s][self.daily_data[s].index == str(date)].tradestatus.values[0] == 0:
                stock_value += float(self.daily_data[s][self.daily_data[s].index == str(date)]['preclose']) * float(
                    self.hold_stock[self.hold_stock.code == s]['size'])
                continue
            if int(self.hold_stock[self.hold_stock.code == s]["size"]) != 0:
                self.stop_profit(s, date)
            if int(self.hold_stock[self.hold_stock.code == s]["size"]) != 0:
                self.stop_loss(s, date)
            stock_value += float(self.daily_data[s][self.daily_data[s].index == str(date)]['close']) * float(
                self.hold_stock[self.hold_stock.code == s]['size'])
        self.total_money.append(stock_value + self.remain_money)

    def Cacul_Performance(self):
        """
        Calculate annualized return, Sharpe ratio, maximal drawdown, return volatility and sortino ratio
        :return: annualized return, Sharpe ratio, maximal drawdown, return volatility and sortino ratio
        """
        rtn = self.total_money[-1] / self.capital - 1

        annual_rtn = np.power(rtn + 1, 252.0 / self.DAY_MAX) - 1  # 复利

        annual_lst = [(self.total_money[k + 1] - self.total_money[k]) / self.total_money[k] for k in
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

        backtest_return = self.total_money[-1] / self.capital - 1
        calmar_ratio = - annual_rtn / max_drawdown_ratio
        # Plot
        print('Net Return: %.2f%%' % (backtest_return * 100.0))
        print('Annualized Return: %.2f%%' % (annual_rtn * 100.0))
        print('Maximal Drawdown: %.2f%%' % (max_drawdown_ratio * 100.0))
        print('Annualized Vol: %.2f%%' % (100.0 * annual_vol))
        print('Sharpe Ratio: %.4f' % sharpe_ratio)
        print('Sortino Ratio: %.4f' % sortino_ratio)
        print('Calmar Ratio: %.4f' % calmar_ratio)
        self.compare()
        plt.figure(figsize=(15, 5.73))
        plt.plot([str(i) for i in self.day], np.array(self.total_money[1:]) / self.capital, label='Strategy Return')
        plt.plot([str(i) for i in self.day], self.reference['close'] / self.reference['close'].iloc[0],
                 label='SH Index')
        plt.plot([str(i) for i in self.day], self.reference['close.1'] / self.reference['close.1'].iloc[0],
                 label='SZ Index')
        plt.plot([str(i) for i in self.day], self.reference['close.2'] / self.reference['close.2'].iloc[0],
                 label='Smallcap 500 index')
        plt.plot([str(i) for i in self.day], self.reference['close.3'] / self.reference['close.3'].iloc[0],
                 label='SSE 50')
        plt.xticks([str(self.day[i]) for i in range(0, len(self.day) - 1, 80)], rotation=20)
        plt.xlabel('Date')
        plt.ylabel('Return Rate')
        plt.title('Investment Return Curve')
        plt.legend(loc='upper left')
        plt.grid(True)
        #         plt.rcParams['font.sans-serif']=['Heiti TC']
        #         plt.rcParams['axes.unicode_minus'] = False
        plt.show()

    def compare(self):

        self.reference = self.reference.loc[self.start:self.end, ]

    def Run(self):
        for d in self.day:
            self.strategy(d)
            self.Update(d)

        self.DAY_MAX = len(self.total_money)
        self.Cacul_Performance()

    def select_stock(self, date):

        '''fin_data选股'''
        self.select_list = set(self.can_trade[date])
        self.select_list = self.select_list.intersection(self.Accessible)
        # 要选波动率低的80%
        self.select_list = self.select_list.intersection(
            set(self.Factor_matrix['ROE波动'][self.Factor_matrix['ROE波动'][date].dropna().tolist()].index))

        # 要ROE要大于10%
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_FA_ROE_TTM'] > 10].index))

        # 删去ROE最高的10%
        self.select_list = self.select_list.intersection(set(self.fin_data[date][
                                                                 self.fin_data[date]['S_FA_ROE_TTM'] < np.percentile(
                                                                     self.fin_data[date]['S_FA_ROE_TTM'].dropna(),
                                                                     90)].index))
        # 毛利率20
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_QFA_GROSSPROFITMARGIN'] > 20].index))

        # 二：成长性
        # 归母净利润提升（单季度）
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_FA_YOYNETPROFIT'] > 0].index))

        # 利率连续增长两期
        self.select_list = self.select_list.intersection(set(self.Factor_matrix['ROE连续两期增长']
                                                             [self.Factor_matrix['ROE连续两期增长'][
                date].dropna().tolist()].index))

        # ROE连续增长两期
        self.select_list = self.select_list.intersection(set(self.Factor_matrix['毛利润连续两期增长']
                                                             [self.Factor_matrix['毛利润连续两期增长'][
                date].dropna().tolist()].index))

        # 营业总收入同比增长 0-90%
        self.select_list = self.select_list.intersection(set(self.fin_data[date][(
                self.fin_data[date]['S_FA_YOY_TR'] < np.percentile(self.fin_data[date]['S_FA_YOY_TR'].dropna(),
                                                                   90))].index))

        # 净利润TTM同比增长10%以上
        self.select_list = self.select_list.intersection(set(self.Factor_matrix['净利润增长率']
                                                             [self.Factor_matrix['净利润增长率'][
                date].dropna().tolist()].index))

        # 三：估值
        # PE小于40
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_VAL_PE_TTM'] < 50].index))
        #         # PE历史分位数60%
        self.select_list = self.select_list.intersection(
            set(self.Factor_matrix['PE历史分位'][self.Factor_matrix['PE历史分位'][date].dropna().tolist()].index))

        # 资产负债率小于60%
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_FA_DEBTTOASSETS'] < 60].index))
        # 经营现金流为正
        self.select_list = self.select_list.intersection(
            set(self.fin_data[date][self.fin_data[date]['S_FA_YOYOCFPS'] > 0].index))

        error = set(['001914.SZ', '002281.SZ', '001872.SZ'])
        self.select_list = self.select_list.difference(set(error))
        return list(self.select_list)

    def strategy(self, date):
        # 选定的交易日（为财报发布日期）

        self.trading_day = self.statDate
        # 首先卖出
        if date in self.trading_day:  # 只有日期等于这几天才会调仓
            # 选股计算权重
            i = np.argwhere(np.array(self.trading_day) == date)[0][0]
            self.selected_slist = self.select_stock(self.statDate[i])

            temp_list = self.fin_data[self.statDate[i]][
                self.fin_data[self.statDate[i]]['Code'].isin(self.selected_slist)]
            #             self.weight = {i: j for i, j in zip(temp_list.index, temp_list['当日流通市值'] / np.sum(temp_list['当日流通市值']))}

            self.weight = {i: np.minimum(1 / len(temp_list.index), 0.15) for i in temp_list.index}
            sell_list = set(self.hold_stock['code']).difference(self.selected_slist)
            if self.Index[self.Index['时间'] == str(date)]['PE increase rate'].values[0] >= 0.10:
                print("Market estimate is too high, we decide to reduce our position")

                for stock in sell_list:
                    self.Sell(date, 0, stock, self.daily_data[stock].loc[str(date), 'close'])
                # 70%空仓
                for stock in self.selected_slist:
                    num = int(
                        (self.weight[stock] * self.remain_money * 0.3 / self.daily_data[stock].loc[
                            str(date), 'close']) / 100)
                    print("buy {} shares of {}  \n".format(num, stock))
                    self.Add_Open(date, num * 100, stock, self.daily_data[stock].loc[str(date), 'close'])

            else:

                # 选定需要出售的股票，仓位的微调交给买入函数

                for stock in sell_list:
                    self.Sell(date, 0, stock, self.daily_data[stock].loc[str(date), 'close'])

                # 调仓买入

                for stock in self.selected_slist:
                    print(stock, date)
                    num = int(
                        (self.weight[stock] * self.remain_money / self.daily_data[stock].loc[str(date), 'close']) / 100)
                    print("buy {} shares of {}  \n".format(num, stock))
                    self.Add_Open(date, num * 100, stock, self.daily_data[stock].loc[str(date), 'close'])


if __name__ == '__main__':
    Data = Data_obtain('./All_stocks_trade', start='20090425', end='20200731')
    M = BackTestModel(Data)
    M.Run()
