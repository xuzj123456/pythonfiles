# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# 设置中文显示
font = {'family': 'SimHei',
        'weight': 'bold',
        'size': '12'}
plt.rc('font', **font)  # pass in the font dict as kwargs
plt.rc('axes', unicode_minus=False)


class Pd_Info:

    """
    月份数据 生成同步序列，及对数同比
    """
    def get_data_sy(self, df, step):

        # 同比步长，12个月
        df_2 = df.shift(step)
        df_sy = np.log(df / df_2)
        df_ln = np.log(df_2)
        df_sy = df_sy / df_ln
        df_all = pd.concat([df, df_ln, df_sy], axis=1)
        df_all.columns = [1, 2, "%s_对数同比"%df.name]
        # ax = df_all.plot(use_index=True, y=[1,  3], secondary_y=[ 3], figsize=(12, 9), title="对数同步序列")
        # ax.set_ylabel("date")
        # ax.right_ax.set_ylabel("同比")
        # plt.grid(True)
        # plt.show()

        return [df, df_ln, df_sy * 100]

    """
    从csv/xls中，获取原始数据
    """
    def get_data_file(self,file_name):
        
        if re.search("xls",file_name,re.I):
            df_ = pd.read_excel(file_name)
        elif  re.search("csv$",file_name,re.I):
            df_ = pd.read_csv(file_name, engine = 'python', encoding = 'utf-8')
        if "date" in df_.columns.tolist():
            df_['date'] = pd.to_datetime(df_['date'])
            df_['date'] = df_['date'].map(lambda x: x.strftime('%Y-%m'))
            df_=df_.set_index(["date"])
        return df_
    

    """
    从csv/xls中，获取原始数据
    日数据转为月数据
    flag:'last'取最后一天
         "first"取第一天
    
    """
    def data_day2month(self, file_name,flag="last"):
        
        if re.search("xls",file_name,re.I):
            df = pd.read_excel(file_name)
        elif  re.search("csv$",file_name,re.I):
            df = pd.read_csv(file_name, engine = 'python', encoding = 'utf-8')
        else:
            raise("数据文件格式错误，需要为csv、xls、xlsx！！")
        df = df.dropna(axis=1,how='all')  # 去除空列
        # 将天换成月
        if "date" in df.columns.tolist():
            df['date'] = pd.to_datetime(df['date'])
            df['date'] = df['date'].map(lambda x: x.strftime('%Y-%m'))
            df_ = df.drop_duplicates('date', flag)
            df_= df_.set_index(["date"])

            return df_
        else:
            raise("数据  日期列名需要为date ！！")
        
    """
    直线拟合
    """
    def get_straight_cur(self, df_sy):
        df_old = df_sy.copy()
        if type(df_sy) is np.ndarray:
            df_sy = pd.Series(df_sy, range(len(df_sy)))
        else:
            df_sy.index = range(len(df_sy))
        # 拟合直线
        from scipy.optimize import curve_fit

        # 创建函数模型用来生成数据
        def func(x, a, b):
            fu = a * x + b
            return fu

        # 待拟合数据
        x = df_sy.index
        y = df_sy
        # 使用curve_fit函数拟合噪声数据
        popt, pcov = curve_fit(func, x, y)
        # 输出给定函数模型func的最优参数
        # print(popt)
        df_func = []
        for i in df_sy.index:
            df_func.append(func(i, popt[0], popt[1]))
        df_cur = pd.Series(df_func, df_old.index)
        df_new = df_old - df_cur

        df_all = pd.concat([df_new, df_old, df_cur], axis=1)
        df_all.columns = ["new", "old", "fit"]
        ax = df_all.plot(use_index=True, figsize=(12, 5), title=u"趋势情况")
        ax.set_ylabel(u"%")
        ax.set_xlabel(u"日期")
        xticks = range(0, len(df_all), 6)
        xticklabels = [df_all.index[i] for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=70)  # roration 旋转

        return df_new

    """
    去趋势，减去拟合的直线
    
    """
    def get_avg_std(self, df):
        # 去趋势
        df_cur = self.get_straight_cur(df.dropna())  # 直线拟合
        df_cur.name = df.name
        return df_cur



    #补零
    def add_zero(self,list_,len_df):
        list_=list_.copy()
        for i in range(len_df-len(list_)):
            list_.append(0)
        return list_

    """"
    hp滤波
    x,年为100，季度为1600，月度为14400
    """
    def hp_lb(self,pf,x=14400 ,flag=False):
        #Y=(I+xF)G
        # 1:  1,-2,1
        #2:   -2,5,-4,1
        #3:   1,-4,6,-4,1
        #4:     1,-4,6,-4,1

        lenth_pf=len(pf)
        half_len = (lenth_pf + 1) // 2
        Y=np.mat(pf).T
        F_list=[]
        if lenth_pf<5:
            print("too short data")
            return
        else:
            f_1=[[1,-2,1],
                [-2,5,-4,1],
                [1,-4,6,-4,1]]
            for i in range(half_len):
                if i <3:
                    F_list.append(self.add_zero(f_1[i],lenth_pf))
                else:
                    f_i=self.add_zero(self.add_zero([],i-2)+f_1[2],lenth_pf)
                    F_list.append(f_i)

            #对称填充
            for i in range(lenth_pf//2-1,-1,-1):
                F_list.append(F_list[i][::-1])

            #求出趋势G，周期C
            F=np.mat(F_list)
            I=np.identity(lenth_pf)
            B=I+x*F
            G=B.I*Y
            C=x*F*G

            df_g=pd.Series(G.T.tolist()[0],pf.index,name="%s hp滤波_趋势要素G"%pf.name)
            df_c=pd.Series(C.T.tolist()[0],pf.index,name="%s hp滤波_周期要素C"%pf.name)
            pf_hp=pd.concat([pf,df_g,df_c],axis=1)
            cols = pf_hp.columns.tolist()
            #画图
            if flag ==True:
                ax = pf_hp.plot(use_index=True, y=cols, secondary_y=cols[-1:], figsize=(10, 5), title="hp滤波 (lambda=%s)"%x)
                #ax.set_ylabel("指数")
                #ax.right_ax.set_ylabel("趋势")
                plt.grid(True)
                #plt.show()

            return df_g,df_c


    def show_from_df(self,pd):
        ax = pd.plot(use_index=True, figsize=(12, 5), title=u"趋势情况")
        # ax.set_xlabel(u"日期")
        # xticks = range(0, len(pd), len(pd)//6)
        # xticklabels = [pd.index[i] for i in xticks]
        # ax.set_xticks(xticks)
        # ax.set_xticklabels(xticklabels, rotation=70)  
        plt.legend()
        #plt.show()

    #画图_双轴
    def showe_2_from_df(self,df_all,*args):
        title= "对比图"
        if len(args):
            df_all=df_all[[i for i in args]]
            title= "  ".join(args)
        
        cols=df_all.columns.tolist()
        ax = df_all.plot(use_index=True, y=cols, figsize=(10, 6),secondary_y=cols[1:], title=title)
        ax.grid(True)

        # xticks = range(0, len(df_all), 6)
        # xticklabels = [df_all.index[i] for i in xticks]
        # ax.set_xticks(xticks)
        # ax.set_xticklabels(xticklabels, rotation=60)  # roration 旋转

