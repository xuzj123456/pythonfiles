# coding=utf-8
from chinese_calendar import is_workday
import numpy as np
import pandas as pd
from datetime import date, timedelta
from scipy.stats import norm
from math import exp, log, sqrt
N = norm.cdf
n = norm.pdf

def is_tradeday(date0):
    # 判断是否为交易日, 传入一个 datetime.date 类型
    if is_workday(date0) and date0.weekday()<5:
        return True
    else:
        return False

def cal_tradeday(date1, date2):
    # 计算两个日期之间的交易日个数，传入两个 datetime.date 类型

    # 确保 date1 < date2
    if date1 >date2:
        d = date1
        date1 = date2
        date2 = d

    n = 0  # 两个日期之间的交易日个数
    delta_ = timedelta(days=1)
    while True:
        if date1.day == date2.day:
            break
        date1 += delta_
        if is_tradeday(date1):
            n+=1
    return n


class Option:
    def __init__(self, S0, K, sigma, q, r, t, multi, type):
        # flag = 'call' or 'put'
        # t直接传入交易日数即可
        self.S0 = S0
        self.K = K
        self.sigma = sigma
        self.r = r
        self.q = q
        self.t = t / 245
        self.type = type
        self.multi = multi
        self.disc_r = exp(-self.r * self.t)
        self.disc_q = exp(-self.q * self.t)
        self.d1 = (log(self.S0 / self.K) + (self.r - self.q + self.sigma ** 2 / 2.
                                            ) * self.t) / (self.sigma * sqrt(self.t))
        self.d2 = self.d1 - self.sigma * sqrt(self.t)
        self.delta = self.get_delta() * self.multi
        self.theta = self.get_theta() * self.multi
        self.gamma = self.get_gamma() * self.multi
        self.vega = self.get_vega() * self.multi
        self.cashdelta = self.delta * self.S0
        self.cashgamma = self.gamma * self.S0 * self.S0 / 100
        self.price = self.get_price() * self.multi

    def get_price(self):
        if self.type == 'call':
            price = self.S0 * self.disc_q * N(self.d1) - self.K * self.disc_r * N(self.d2)
        if self.type == 'put':
            price = -self.S0 * self.disc_q * N(-self.d1) + self.K * self.disc_r * N(-self.d2)
        return price

    def get_delta(self):
        if self.type == 'put':
            delta = (N(self.d1) - 1) * self.disc_q
        if self.type == 'call':
            delta = N(self.d1) * self.disc_q
        return delta

    def get_theta(self):
        if self.type == 'call':
            theta = (- self.r * self.K * self.disc_r * N(self.d2)
                     - self.S0 * self.sigma * self.disc_q * n(self.d1) / (2 * sqrt(self.t))
                     + self.q * self.S0 * self.disc_q * N(self.d1)) / 245
        if self.type == 'put':
            theta = (+ self.r * self.K * self.disc_r * N(-self.d2)
                     - self.S0 * self.sigma * self.disc_q * n(self.d1) / (2 * sqrt(self.t))
                     - self.q * self.S0 * self.disc_q * N(-self.d1)) / 245
        return theta

    def get_gamma(self):
        gamma = self.disc_q * n(self.d1) / (self.S0 * self.sigma * sqrt(self.t))
        return gamma

    def get_vega(self):
        vega = self.S0 * self.disc_q * n(self.d1) * sqrt(self.t) / 100
        return vega


if __name__ == '__main__':
    pos = pd.read_csv('20200930154324-Portfolio.csv')

    c = Option(4.572756, 4.26, 0.314, 0.0561, 0.025, cal_tradeday(date(2020,9,30), date(2020,10,28)), 10330, 'call')
    P = Option(4.572756, 4.26, 0.314, 0.0561, 0.025, cal_tradeday(date(2020,9,30), date(2020,10,28)), 10330, 'put')