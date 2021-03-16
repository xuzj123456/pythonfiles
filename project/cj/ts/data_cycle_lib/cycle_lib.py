#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math,cmath
from scipy.fftpack import fft,ifft
from scipy.optimize import curve_fit
from sklearn import linear_model

#设置中文显示
font = {'family' : 'SimHei',
    'weight' : 'bold',
    'size'  : '12'}
plt.rc('font', **font) # pass in the font dict as kwargs
plt.rc('axes',unicode_minus=False)


class Cycle_PF:
    def __init__ (self, pd,Fs):
        self.df_sy = pd
        self.f_s = Fs                                  #采样频率(按年) 
        
    #傅里叶变换
    def __get_fft(self):
        df_sy=self.df_sy
        f_s = self.f_s                                  #采样频率(按年)    
        """
        #采样间距（采样率的倒数）
        #如果采样间隔以秒为单位，则频率单位为周期/秒。给定长度n和样本间距d：
        """
        freqs = np.fft.fftfreq(len(df_sy),1/f_s)  
        df_fft = np.fft.fft(df_sy)                #快速傅里叶变换
        
        return df_fft,freqs
        
    #高斯滤波器
    def __imgGaussian_new(self,u,sigma,freqs):
        gpl = np.exp(- ((freqs - u) / (2 * sigma)) ** 2)
        gmn = np.exp(- ((freqs + u) / (2 * sigma)) ** 2)  
        gaussian_mat=gpl+gmn
        
        return gaussian_mat



    #傅里叶反变换
    def __get_ifft(self,T,df_fft,freqs):
        
        #高斯过滤
        gau_data=self.__imgGaussian_new(self.f_s / T, self.f_s/( len(df_fft)), freqs)
        df_by_gau = []
        for i in range(len(df_fft)):
            yy_flag_item=df_fft[i]
            df_by_gau.append( yy_flag_item* gau_data[i])
        ifft_by_gau = ifft(df_by_gau) #傅里叶反变换
        ifft_df=pd.Series(ifft_by_gau.real,self.df_sy.index)
        ifft_df.name =T
        
        return ifft_df
    
    
    #获取幅值最高三个峰对应的周期
    def get_fft_top(self,n=3):
        df_fft,freqs=self.__get_fft()
        df_fft_abs = abs(df_fft)      
        #对称数据，取一半数据
        freqs = freqs[:len(freqs)//2]
        df_fft_abs = df_fft_abs[:len(df_fft_abs)//2]
        
        index_data_all = []
        #求局部峰值
        for i in range(1,len(df_fft_abs)-1,1):
            if df_fft_abs[i]>df_fft_abs[i-1] and df_fft_abs[i]>df_fft_abs[i+1]:
                index_data_all.append(i)
                i+= 2
            else:
                i+=1
        
        pd_fft = pd.DataFrame({
        'freqs': freqs,
        'fft_abs': df_fft_abs})
        #print("pd_fft",pd_fft)
        pd_top = pd_fft.iloc[index_data_all,].sort_values(by="fft_abs",ascending = False)
        #print("pd_top",pd_top)
        #print("pd_top2",100*pd_top["fft_abs"][:3]/pd_fft["fft_abs"].sum().tolist())
        #print("top %s:  "%n,(1/pd_top["freqs"])[:3].tolist())
        return (1/pd_top["freqs"])[:3].tolist(),(100*pd_top["fft_abs"][:3]/pd_fft["fft_abs"].sum()).tolist()
    
    
    #傅里叶变换
    def show_fft(self):
        df_fft,freqs=self.__get_fft()
        df_fft_abs = abs(df_fft)            #幅度
        df_sy=self.df_sy
        
        plt.figure(figsize=(12,5))
        plt.subplot(121)
        ax=df_sy.plot(title='%s原始序列'%df_sy.name)
        ax.set_xlabel(u"日期")
        # xticks = range(0, len(df_sy), len(df_sy)//6)
        # xticklabels = [df_sy.index[i] for i in xticks]
        # ax.set_xticks(xticks)
        # ax.set_xticklabels(xticklabels, rotation=70)  # roration 旋转

        plt.subplot(122)
        plt.plot(freqs, df_fft_abs, 'r')
        plt.title('%s傅里叶变换后频谱图'%df_sy.name)
        plt.xlabel('频率 月（-1）')
        plt.ylabel('幅度')
        plt.grid(True)
        plt.show()
        
    #周期滤波
    def cycle_filter(self,*args):
        # 傅里叶变换
        df_fft, freqs = self.__get_fft()  #快速傅里叶变换，频率
        filter_dfs=[]
        for item_t in args:
            filter_dfs.append(self.__get_ifft(item_t,df_fft,freqs))
        
        return filter_dfs
    
    def show_cycle_filter(self,*args):
        df_sy=self.df_sy
        filter_dfs=self.cycle_filter(*args)
        pf_all=[df_sy]+filter_dfs
        
        
        name_str=("%s月 "*len(args))%args
        #周期滤波后，画图
        df_all = pd.concat(pf_all, axis=1, sort=False)
        ax_1 = df_all.plot(use_index=True
                           , figsize=(12, 6), title=u"%s高斯滤波后  周期："%df_sy.name+name_str)
        ax_1.set_xlabel(u"日期")
        #ax_1.set_ylabel(u"单位（%）")
        ax_1.grid(True)
        # xticks = range(0, len(df_all), 6)
        # xticklabels = [df_all.index[i] for i in xticks]
        # ax_1.set_xticks(xticks)
        # ax_1.set_xticklabels(xticklabels, rotation=70)  # roration 旋转
        
        #plt.show()

    """
    按照指定周期高斯滤波
    参数：周期（月）
    返回：拟合图形
    """
    def cycle_by_gau(self,*args):
    
        #周期滤波
        # 傅里叶变换
        df_fft, freqs = self.__get_fft()  #快速傅里叶变换，频率
        df_by_gau = np.zeros(len(df_fft))
        #print("df_by_gau",df_by_gau)
        for item_t in args:
            #高斯过滤
            gau_data=self.__imgGaussian_new(self.f_s / item_t, self.f_s/( len(df_fft)), freqs)
            print("df_by_gau111",np.array(df_fft)*np.array(gau_data))
            df_by_gau = np.array(df_fft)*np.array(gau_data) +df_by_gau
            
            # for i in range(len(df_fft)):
                # yy_flag_item=df_fft[i]
                # df_by_gau.append( yy_flag_item* gau_data[i])
            #filter_fft.append(df_by_gau)
        ifft_by_gau = ifft(df_by_gau) #傅里叶反变换
        
        ifft_df=pd.Series(ifft_by_gau.real,self.df_sy.index)
        ifft_df.name =self.df_sy.name +("%s月 "*len(args))%args
        
        fiter_dfs = ifft_df
        if not len(fiter_dfs):
            print("周期滤波 为空")
            return
        
        #画图
        # df_all_fit = pd.concat([self.df_sy,fiter_dfs ], axis=1, sort=False)
        # ax_2 = df_all_fit.plot(use_index=True
                           # , figsize=(12,6), title=u"%s  高斯滤波后，周期："%self.df_sy.name+ifft_df.name)
        # ax_2.set_xlabel(u"日期")
        # #ax_2.set_ylabel(u"单位（%）")
        # ax_2.grid(True)
        # # xticks_2 = range(0, len(df_all_fit), 6)
        # # xticklabels_2 = [df_all_fit.index[i] for i in xticks_2]
        # # ax_2.set_xticks(xticks_2)
        # # ax_2.set_xticklabels(xticklabels_2, rotation=70)  # roration 旋转
        
        
        return fiter_dfs    
        
        
    """
    按照指定周期高斯滤波后，进行回归拟合
    参数：周期（月）
    返回：拟合图形
    """
    def cycle_fit_by_gau(self,*args):
    
        #周期滤波
        fiter_dfs=self.cycle_filter(*args)
        if not len(fiter_dfs):
            print("周期滤波 为空")
            return
        #待拟合数据
        X =[]
        for i in range(len(fiter_dfs[0])):
            df_list=[]
            for item in fiter_dfs:
                df_list.append(item[i])
            X.append(df_list)
        
        #调用模型
        clf = linear_model.LinearRegression()
        Y = self.df_sy
        #训练模型
        clf.fit(X,Y)

        # 拟合值
        y_hat = clf.predict(X)
        
        
        three_fit_df=pd.Series(y_hat,Y.index)
        three_fit_df.name="%s_fit"%Y.name
        
        # ##画图
        # name_str=("%s月 "*len(args))%args
        # df_all_fit = pd.concat([Y,three_fit_df ], axis=1, sort=False)
        # ax_2 = df_all_fit.plot(use_index=True
                           # , figsize=(12,6), title=u"%s  高斯滤波后，线性回归合成，周期："%Y.name+name_str)
        # ax_2.set_xlabel(u"日期")
        # #ax_2.set_ylabel(u"单位（%）")
        # ax_2.grid(True)
        
        #更改坐标
        # # xticks_2 = range(0, len(df_all_fit), 6)
        # xticklabels_2 = [df_all_fit.index[i] for i in xticks_2]
        # ax_2.set_xticks(xticks_2)
        # ax_2.set_xticklabels(xticklabels_2, rotation=70)  # roration 旋转
        
        
        return three_fit_df

    """
    简单拟合
    按照2个余弦进行拟合
    """
    def cycle_simple_fit(self,t1,t2):
        df_sy=self.df_sy
        df_old=df_sy.copy()
        
        df_sy.index=range(len(df_sy))
        
        # 创建函数模型用来生成数据
        def func(x, a, b, c, d, e):
            fu = a * np.cos(np.pi * (2/ t1) * x + d) + b * np.cos(np.pi * (2 / t2) * x + e) - c
            return fu

        # 待拟合数据
        x = df_sy.index
        y = df_sy

        popt, pcov = curve_fit(func, x, y)
        df_func = []
        for i in df_sy.index:
            df_func.append(func(i, popt[0], popt[1], popt[2], popt[3], popt[4]))

        simple_fit_df = pd.Series(df_func, df_old.index)
        simple_fit_df.name = "simple_fit  %s and %s" %(t1,t2)

        df_all_fit = pd.concat([df_old, simple_fit_df], axis=1, sort=False)
        ax_2 = df_all_fit.plot(use_index=True
                               , figsize=(12, 6), title=u'简单周期模拟情况%s 和%s'%(t1,t2))
        ax_2.set_xlabel(u"日期")
        ax_2.grid(True)
        # xticks_2 = range(0, len(df_all_fit), 6)
        # xticklabels_2 = [df_all_fit.index[i] for i in xticks_2]
        # ax_2.set_xticks(xticks_2)
        # ax_2.set_xticklabels(xticklabels_2, rotation=70)  # roration 旋转

        # plt.figure(figsize=(12,5))
        # plt.title('简单周期模拟情况%s 和%s'%(t1,t2))
        # plt.xlabel('iteration times')
        # plt.ylabel('sy_rate')
        # plt.plot(df_old.index, df_func, color='green', label='new')
        # plt.plot(df_old.index, df_sy, color='red', label='original')
        #
        # plt.legend()  # 显示图例
        plt.show()

"""
求取标准化谱密度函数

"""       
class PU_Cycle_PF:
    def __init__ (self, pd,M,L):
        self.df_sy = pd           #样本
        self.N = len(self.df_sy)  #样本长度
        self.M = M                #窗参数
        self.L = L                #频率点个数 ，一般建议取序列长度的一半
        self.f = np.array([j/(2*self.L) for j in range(0,self.L+1)])  #得到频率点
        self.get_pu_function()
    
    #获取幅值最高2个峰对应的周期
    def __get_fft_top(self,pf,n=2):
        freqs = pf.index
        df_fft_abs = np.array(pf)
        index_data_all = []
        #求局部峰值
        for i in range(1,len(df_fft_abs)-1,1):
            if df_fft_abs[i]>df_fft_abs[i-1] and df_fft_abs[i]>df_fft_abs[i+1]:
                index_data_all.append(i)
                i+= 2
            else:
                i+=1
        
        pd_fft = pd.DataFrame({
        'freqs': freqs,
        'fft_abs': df_fft_abs})
        
        pd_top = pd_fft.iloc[index_data_all,].sort_values(by="fft_abs",ascending = False)[0:n]
        #print("pd_top     ",pd_top)
        return pd_top
    
    #获取自协方差函数    
    def  __get_cov_function(self,k):
        
        x = self.df_sy.mean()  #样本均值
        xt = np.array(self.df_sy[:self.N-k]-x)
        xtk = np.array(self.df_sy[k:self.N]-x)
        R = sum(xt*xtk)/self.N  
        
        return R    
    
    #获取hanning函数
    def __get_w_function(self,k):
        if abs(k) <= self.M:
            return 0.5+0.5*math.cos(k*math.pi/self.M)
        else:
            return 0

    def __plot_pu_pf(self,pf):
        top_data = np.array(self.__get_fft_top(pf)) #获取峰值
        #画图
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot(111)
        ax.set_title('%s 标准谱分析(参数 M:%s  N:%s  L:%s)'%(self.df_sy.name,self.M,self.N,self.L))
        ax.set_xlabel('f')
        ax.set_ylabel('p(f)')
        ax.plot(pf.index, pf, color='black',markerfacecolor='red',marker='o') 
        for a, b in top_data: 
            ax.axvline(a,linestyle="--") #画辅助线
            #ax.plot([a, b],[a,0],linestyle="--")
            ax.text(a, b, ("T= %s"%(1/a)),ha='left', va='bottom', fontsize=12) #峰值注释 
          
        plt.show()
    
    
    #标准化谱密度函数
    def get_pu_function(self):
        pf_list = []
        wk = np.array([self.__get_w_function(k) for k in range(1,self.M+1)])
        rk = np.array([self.__get_cov_function(k)/self.__get_cov_function(0) for k in range(1,self.M+1)])
        
        for fi in self.f:
            cos = np.array([math.cos(2*math.pi*fi*k) for k in range(1,self.M+1)])
            pf_list.append( 1+2*sum(wk*rk*cos))
        
        pf = pd.Series(pf_list,self.f)
        self.__plot_pu_pf(pf)  #画图
        
        return pf
        
    
"""
MARPLE 算法 进行谱分析

"""       
class MARPLE_PU_Cycle_PF:
    def __init__ (self, pd,fs,P):
        self.df_sy = pd           #样本
        self.M = len(self.df_sy)  #样本长度
        self.fs = fs              #采样率
        self.P = P                #阶数
        self.new_pf = None
        #self.get_marple_function()
    
    #获取幅值最高2个峰对应的周期
    def __get_fft_top(self,pf,n=2):
        freqs = pf.index
        df_fft_abs = np.array(pf)
        index_data_all = []
        #求局部峰值
        for i in range(1,len(df_fft_abs)-1,1):
            if df_fft_abs[i]>df_fft_abs[i-1] and df_fft_abs[i]>df_fft_abs[i+1]:
                index_data_all.append(i)
                i+= 2
            else:
                i+=1
        
        pd_fft = pd.DataFrame({
        'freqs': freqs,
        'fft_abs': df_fft_abs})
        
        pd_top = pd_fft.iloc[index_data_all,].sort_values(by="fft_abs",ascending = False)[0:n]
        #print("pd_top     ",pd_top)
        return pd_top
    
    #获取c函数    
    def  __get_c_function(self,i,j):
        M = self.M
        P = self.P
        
        xni = np.array(self.df_sy[P-i:M-1-i])
        xnj = np.array(self.df_sy[P-j:M-1-j])
        xnpi = np.array(self.df_sy[i:M-1-P+i]) 
        xnpj = np.array(self.df_sy[j:M-1-P+j])
        #print("i,j,xni",i,j,xni,xnj,xnpi,xnpj)
        C = sum(xni*xnj)+ sum(xnpi*xnpj)
        return C    
    
    def __plot_ar_pf(self,pf):
        top_data = np.array(self.__get_fft_top(pf)) #获取峰值
        #AR谱分析画图
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot(111)
        ax.set_title('%s AR谱分析(参数 fs:%s  P:%s )'%(self.df_sy.name,self.fs,self.P))
        ax.set_xlabel('f')
        ax.set_ylabel('p(f)')
        ax.plot(pf.index, pf, color='black',markerfacecolor='red',marker='o') 
        for a, b in top_data: 
            ax.axvline(a,linestyle="--") #画辅助线
            #ax.plot([a, b],[a,0],linestyle="--")
            ax.text(a, b, ("T= %s"%(1/a)),ha='left', va='bottom', fontsize=12) #峰值注释 
        plt.show()
    
    
    
        
    #marple算法
    def get_marple_function(self):
        cp = np.ones((self.P,self.P))
        for i in range(0,self.P):
            for j in range(0,self.P):
                cp[i][j] = self.__get_c_function(i+1,j+1)
        b = np.ones(self.P)
        for i in range(0,self.P):
            b[i] = self.__get_c_function(i+1,0)
        #转换为矩阵
        cp_mat = np.matrix(cp)
        b_mat = np.matrix(b)
        
        am = -b_mat*(cp_mat.I).T #得到参数矩阵
        aml = np.array(am)[0]
        print("am1",aml)
        
        #根据得到的参数a，重构信号
        new_list = []
        old_df = np.array(self.df_sy)
        for i in range(len(old_df)):
            if i<self.P:
                new_list.append(old_df[i])
            else:
                new_item = sum(-old_df[i-self.P:i][::-1]*aml)
                new_list.append(new_item)
            
        #self.new_pf = pd.Series(new_list,self.df_sy.index) #重构信号
        
        new_var = np.var(old_df-np.array(new_list)) #方差
        rss = sum((old_df-np.array(new_list))**2)
        print("end  var      ",new_var)
        # new_var1 = self.__get_c_function(0,0) - sum(aml*[self.__get_c_function(0,i) for i in range(1,self.P+1,1)])
        # print("end  var1      ",new_var1)
        
        #返回 参数 和方差
        return aml,new_var,rss
        
        
        #谱分析计算
    def get_mar_pu_function(self):
        aml,new_var,rss = self.get_marple_function()
        #根据得到的参数a，重构信号并预测
        new_list = []
        old_df = np.array(self.df_sy)
        for i in range(len(old_df)+self.P):
            if i<self.P:
                new_list.append(old_df[i])
            elif i<len(old_df):
                new_item = sum(-old_df[i-self.P:i][::-1]*aml)
                new_list.append(new_item)
            else:
                new_item = sum(-np.array(new_list[i-self.P:i][::-1])*aml)
                new_list.append(new_item)
            
        self.new_pf = pd.Series(new_list,range(len(new_list))) #重构信号,并预测
        print("self.new_pf",self.new_pf)
        
        #self.new_pf.plot()
        #self.df_sy.index = range(len(self.df_sy))
        self.df_sy.plot() 
        #频率
        f_range = np.array([j*self.fs/self.M for j in range(1,(self.M+1)//2+1)])
        pu_list = []
        for f in f_range:
            pu_list.append( new_var/abs(1+sum(aml*np.array([cmath.exp(-(1j*2*math.pi*f*i)/self.fs) for i in range(1,self.P+1,1)])))**2)
        
        ar_pu_pf = pd.Series(pu_list,f_range)
        self.__plot_ar_pf(ar_pu_pf)
        
        
        return ar_pu_pf
        
        
        
"""
X11 算法 提出趋势季节要素

输入：时间序列，模型：加法 or 乘法

"""       
class X11_TEST:
    def __init__ (self, pd):
        self.df_sy = pd           #样本
        self.M = len(self.df_sy)  #样本长度
        self.fs = fs              #采样率
        self.P = P                #阶数
        self.new_pf = None
        #self.get_marple_function()
    
    
    def __get_chazhi(self,pd,left_n,right_n):
        pass
        
    
    #12个月中心化移动平均计算暂定的趋势循环要素
    def __get_12_move(self):
        TC1 =""
        pass
        
        
        
        
        
        
        
        