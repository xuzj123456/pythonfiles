#-*- coding:utf-8 -*-
import data_cycle_lib.data_clean_lib as  clean_tool
import data_cycle_lib.cycle_lib as cycle_tool
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np
import re
import time
from random import randint, sample
import traceback

import multiprocessing


"""
获取最优的person相关系数,TS,KL
"""
def get_data_corr(df_1,df_2,move_len):
    #存在数据为nan和inf的，去掉
    
    pd_two = pd.concat([df_1,df_2],axis=1,sort =True)
    pd_two = pd_two.replace([np.inf, -np.inf], np.nan).dropna()
    
    
    item_list_00 = get_best_corr(pd_two,move_len)      #获取最优person平移
    item_list_00 += time_diff_corr_new(pd_two,move_len)    #获取最优TS
    item_list_00 += ["kl","kl","kl","kl"]   #KL注释掉
    #item_list_00 += __k_l_info(pd_two,move_len)          #获取最优KL
    #0,3,6位移TS
    for i in [0,3,6]:
        item_list_00 += __get_per_ts_kl(pd.concat([df_1,df_2.shift(i)],axis=1,sort=True))
    
    #获取显著的3个周期频率
    freqs_list_1 =[]
    freqs_list_2 =[]
    
    base_cycle_1=cycle_tool.Cycle_PF(df_1,1)  #周期
    freqs_list_1 = base_cycle_1.get_fft_top()[0]
    try:
        base_cycle_2=cycle_tool.Cycle_PF(df_2,1)  #周期
        freqs_list_2 = base_cycle_2.get_fft_top()[0]
    except:
        print("err：fft高斯滤波错误",df_2)
    item_list_00 += [str(freqs_list_1),str(freqs_list_2)]
    return item_list_00

"""
平移获取最优的person
"""
def get_best_corr(df,move_len):
    df = df.dropna().replace()
    df_corr_list = []
    df_cols = df.columns.tolist()
    for i in range(-move_len,move_len+1,1):
        df_1=df.copy()
        col_1 = df_cols[1]
        df_1[col_1]=df_1[col_1].shift(i)
        df_corr_shift=df_1.corr().iat[0, 1]
        df_corr_list.append([i,df_corr_shift])
    big_corr=[]
    for item in df_corr_list:
        if not big_corr:
            big_corr=item
        if item[1]>big_corr[1]:
            big_corr=item
    
    return [df_cols[0], df_cols[1],big_corr[0],big_corr[1]]

"""
时差相关分析,计算时间差相关系数
"""    
def time_diff_corr_new(df,move_len):
    tl = move_len  #位移长度
    df = df.dropna()
    n = len(df) #序列长度
    lmax = tl
    lmin = lmax*(-1)
    rel = []
    timel = ""
    cols = df.columns.tolist()
    
    for l in range(lmin,lmax+1):
        df_1 =df.copy()
        df_1[cols[1]]=df_1[cols[1]].shift(l) #位移l
        df_1 = df_1.dropna()
        xmeans = df_1[cols[1]].mean()  #求平均
        ymeans = df_1[cols[0]].mean()  
        x = np.array(df_1[cols[1]])
        y = np.array(df_1[cols[0]]) #基准序列
        d=asum=bsum=0.0   
        asum = np.sum((x-xmeans)*(y-ymeans))
        bsum = np.sum((x-xmeans)*(x-xmeans))*np.sum((y-ymeans)*(y-ymeans))
        d=np.sqrt(bsum)
        if asum==d==0:
            r=0
        else:
            r=asum/d
        rl=abs(r)
        rel.append(rl)#将结果存入rel
        if rl==max(rel):
            timel=l
    return [cols[0], cols[1],timel,max(rel)]   
    
"""
#kl信息量    不能有负数    
"""        
def __k_l_info(df,move_len):
    df = df
    cols = df.columns.tolist()
    
    if df[df.columns[0]].min() <0:
        df[df.columns[0]]=df[df.columns[0]]-df[df.columns[0]].min()+0.00000001
    if df[df.columns[1]].min() <0:
        df[df.columns[1]]=df[df.columns[1]]-df[df.columns[1]].min()+0.00000001
    
    kl_min = 1000000
    index = ""
    for i in range(-move_len,move_len+1,1):
        df_1=df.copy()
        df_1[cols[1]]=df_1[cols[1]].shift(i) #位移
        df_pq = df_1.dropna()
        p=""
        q=""
        p = np.array(df_pq[cols[0]])
        q = np.array(df_pq[cols[1]])
        kl=scipy.stats.entropy(p, q)
        if kl<kl_min:
            kl_min = kl
            index = i
   
    return [cols[0], cols[1],index,kl_min]

"""
获取各种相关系数
"""
def __get_per_ts_kl(df):
    df = df.replace([np.inf, -np.inf], np.nan).dropna()  #去除NAN 和inf
    #皮尔逊相关系数
    df_corr=df.corr().iat[0, 1]
    
    n = len(df) #序列长度
    x = np.array(df[df.columns[1]])
    y = np.array(df[df.columns[0]]) #基准序列
    d=asum=bsum=csum=0.0
    xmeans=np.mean(x)
    ymeans=np.mean(y)
    l=0
    if l>=0:#l为正数时，x由0~n-l,y由l~n
        for i in range(l,n):
            a=(x[i-l]-xmeans)*(y[i]-ymeans)
            b=pow((x[i-l]-xmeans),2)
            c=pow((y[i]-ymeans),2)
            asum=a+asum
            bsum=b+bsum
            csum=c+csum
    d=np.sqrt(bsum*csum)
    if asum==d==0:
        r=0
    else:
        r=asum/d
    ts=abs(r)
    #KL
    kl=""
    if df[df.columns[0]].min() <0:
        df[df.columns[0]]=df[df.columns[0]]-df[df.columns[0]].min()+0.00000001
    if df[df.columns[1]].min() <0:
        df[df.columns[1]]=df[df.columns[1]]-df[df.columns[1]].min()+0.00000001
    df_pq = df
    p=""
    q=""
    p = np.array(df_pq[df_pq.columns[0]])
    q = np.array(df_pq[df_pq.columns[1]])
    kl=scipy.stats.entropy(p, q)
    return [df_corr,ts,kl]   









class CI_AND_DI:
    """
    根据月度数据或者日度数据，获得月度的CI/DI合成指数
    
    两种数据传入方式：
    1、基准数据和指标数据在一个文件中，
    第一列为日期且列名为"date",基准数据在第二列，后面为指标数据
    2、基准数据和指标数据在不同个文件中，需确认文件第一列为日期且列名为"date"
    """
    
    
    
    def __init__ (self,type_dict_file_name=""):
        self.type_dict_name = type_dict_file_name     #指标分类的
        self.indexs_rate_dict = {"经济增长":3,"货币":3,"通胀":2,"基金":1,"其他":1}        #各指标分类所占比例
        
        # # self.index_file_name = index_file_name    #指标名称
        # # self.data_check = ""                      #周期数据
        # # self.best_pd = ""                          #周期数据最优相关系数
        # #self.freqs_list = []  # 基准 fft高斯滤波 频率周期
    
    #hp_滤波，返回周期项
    def hp_lb_c(self,df):
        clean_tool_= clean_tool.Pd_Info()
        step=14400 #月度数据14400
        df =df.dropna()
        return clean_tool_.hp_lb(df,step)[1]
    
    #fft高斯滤波，返回拟合
    def __fft_gau(self,df):
        try:
            base_cycle=cycle_tool.Cycle_PF(df,1)  #周期
            freqs_list = base_cycle.get_fft_top()[0]
            #base_cycle.show_fft()
            #base_cycle.get_fft_top()
            #三周期拟合数据
            base_fit_42_gau=base_cycle.cycle_fit_by_gau(*freqs_list)
        except:
            print("err：fft高斯滤波错误")
            base_fit_42_gau= pd.Series()
        return base_fit_42_gau
    
    
    #设定基准，如果per和TS差距在0.2以内，且per位移为正，则以person为基准
    
    def __set_base_per_or_TS(self,ts_num,pre_num,ts_move,per_move):
        if abs(float(ts_num)-float(pre_num))<0.2 :
            return float(pre_num)*100
        else:
            return float(ts_num)*100
    
   
    #增加打分，优化展示
    def __get_TS_score(self,pf_all):
        #print(list(pf_all))
        name_lists =  ["指标1","指标2",
                    "最优TS位移位数","最优TS",
                    "最优皮尔逊位移位数","最优位移皮尔逊相关系数",
                    "指标1 显著频率top3","指标2 显著频率top3","未位移皮尔逊相关系数","TS","kl"]
        
        pf_base = pf_all[name_lists]
        list_res = []
        for item in np.array(pf_base):
            try:
                if item[3] and item[5] and item[6] and item [7]:
                    #基准为TS*100 或者person *100
                    base_score = self.__set_base_per_or_TS(item[3],item[5],item[2],item[4])
                    item_score = base_score
                    #相关类型 1代表正相关，0代表负相关
                    corr_type = 1
                    #p判断负相关,减5分,（相关系数不等于person相关系数）
                    if item_score!=float(item[5])*100:
                        item_score -=5
                        corr_type = 0
                    #三周期第一周期+-3  -2分
                    #其他-5分
                    #print("===============",item)
                    diff_ = abs(eval(item[7])[0] -eval(item[6])[0])
                    if diff_<3 and diff_>0:
                        item_score -=2
                    elif diff_ >=3:
                        item_score -=5

                    item_list = list(item)
                    item_list.insert(2,item_score)
                    list_res.append(item_list+[corr_type])
            except:
                print("!"*100)
                print("计算相关性得分 错误，请检查数据是否存在空值！！！")
                print("错误信息为：%s"%(str(traceback.format_exc())))
                print(item)
                print("!"*100)
        pf_1 = pd.DataFrame(list_res)
        name_lists_=name_lists+["相关类型(1:正相关_person为基准 ;0:负相关_TS为基准)"]
        name_lists_.insert(2,"相关性得分")
        pf_1.columns = name_lists_

        return pf_1
    
    """
    生成pd
    """
    def __to_pds(self,str_all_list,data_process):
        str_pd_00 = pd.DataFrame(str_all_list)
        str_pd_00.columns = ["指标1","指标2","最优皮尔逊位移位数","最优位移皮尔逊相关系数",
                            "指标1","指标2","最优TS位移位数","最优TS",
                            "指标1——注释","指标2——注释","最优kl位移位数——注释","最优kl——注释",    #注释掉KL
                            "未位移皮尔逊相关系数","TS","kl",
                            "位移3个月皮尔逊","位移3个月TS","位移3个月kl",
                            "位移6个月皮尔逊","位移6个月TS","位移6个月kl",
                            "指标1 显著频率top3","指标2 显著频率top3",
                            ]
  
        #删除重复列
        str_pd_11 = str_pd_00.T.drop_duplicates().T
        pf_1 = self.__get_TS_score(str_pd_11)
        
        return pf_1

    
    """
    数据处理 ：求出最优corr  Ts
    hp: hp滤波得到周期项
    hp_cycle: hp滤波得到3周期
    
    返回：周期数据（pd），最优相关系数数据(pd)
    """
    def get_best_corr_data(self,base_file_name,index_file_name="",move_len=12,data_process ="hp"):
        clean_tool_= clean_tool.Pd_Info()
        #只有一个文件
        if index_file_name=="":
            pf_all = clean_tool_.data_day2month(base_file_name)
            
            pf_all_cols = pf_all.columns.tolist()
            pf_base = pf_all[pf_all_cols[0]]
            pf_indexs = pf_all[pf_all_cols[1:]]
        elif  index_file_name and  base_file_name:
            pf_base = clean_tool_.data_day2month(base_file_name)
            pf_indexs = clean_tool_.data_day2month(index_file_name)
        else:
            raise("参数错误，文件名不对")
        
        
        pf_all_new=pd.concat([pf_base,pf_indexs],axis=1)
        pf_all__new_cols= pf_all_new.columns.tolist()    #列名
        
        data_check = ""
        if data_process=="hp_cycle":
            hp_lb_c_all = pf_all_new.apply(self.hp_lb_c)  #hp_lb
            data_check = hp_lb_c_all.apply(self.__fft_gau)  #高斯滤波
        elif data_process=="hp":
            hp_lb_c_all = pf_all_new.apply(self.hp_lb_c)  #hp_lb
            data_check = hp_lb_c_all
        elif data_process=="original" or data_process=="":
            data_check = pf_all_new
            data_process = "original"
        else:
            raise("data_process  ；只支持 'hp_cycle', 'hp', 'original'3种类型")
        print("data_check",data_check)
        str_all_list=[] 
        print("*"*100)
        print("开始计算相关系数")
        
        #多进程：
        pool = multiprocessing.Pool(processes=4)
        results = []
        for item in pf_all__new_cols[1:]:
            print("-"*50)
            print("%s  和  %s"%(pf_all__new_cols[0],item))
            item_pf = data_check[item].dropna()
            results.append(pool.apply_async(get_data_corr, (data_check[pf_all__new_cols[0]],item_pf,move_len )))
        pool.close() # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join() # 等待进程池中的所有进程执行完毕
        print("="*100,"进程关闭！！！")
        
        for res in results:
            str_all_list.append(res.get())
        
        
        
        # #单进程
        # for item in pf_all__new_cols[1:]:
            # print("-"*50)
            # print("%s  和  %s"%(pf_all__new_cols[0],item))
            # item_pf = data_check[item].dropna()
            # item_list = get_data_corr(data_check[pf_all__new_cols[0]],item_pf,move_len)
            # str_all_list.append(item_list)
        
        best_pd = self.__to_pds(str_all_list,data_process)  #生成 最优相关系数pd
        time_item = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))

        
        data_check_name = "%s_%s原始数据处理后_%s_%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,time_item)
        best_pd_name = "%s_%s最优相关系数_%s_%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,time_item)
        best_pd.to_csv(best_pd_name)   
        data_check.to_csv(data_check_name)
        
        return data_check_name,best_pd_name
        
        
        
    
    """
    数据处理 ：求出最优corr  Ts
    hp: hp滤波得到周期项
    hp_cycle: hp滤波得到3周期
    
    返回：周期数据（pd），最优相关系数数据(pd)
    """
    def get_best_corr_data_from_pd(self,pd_base,pd_index="",move_len=12,data_process ="hp"):
       
        if len(pd_index):
            pf_all_new = pd_base
        elif  len(pd_base) and  len(pd_index):
            pf_all_new=pd.concat([pf_base,pd_index],axis=1)
        else:
            raise("参数错误，文件名不对")
        
        pf_all__new_cols= pf_all_new.columns.tolist()    #列名
        hp_lb_c_all = pf_all_new.apply(self.hp_lb_c)  #hp_lb
        
        data_check = ""
        if data_process=="hp_cycle":
            data_check = hp_lb_c_all.apply(self.__fft_gau)  #高斯滤波
        elif data_process=="hp":
            data_check = hp_lb_c_all
        else:
            raise("data_process  ；只支持 'hp_cycle'和 'hp' 两种类型")
    
        
        str_all_list=[] 
        
        for item in pf_all__new_cols[1:]:
            item_pf = data_check[item].dropna()
            item_list = get_data_corr(data_check[pf_all__new_cols[0]],item_pf,move_len)
            str_all_list.append(item_list)
        best_pd = self.__to_pds(str_all_list,data_process)  #生成 最优相关系数pd
        time_item = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))

        
        data_check.to_csv("%s_%s_原始数据处理后_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item))
        best_pd.to_csv("%s_%s_最优相关系数_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item))   
        return data_check,best_pd
    
    
   
 