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
    
    
    """
    获取最优的person相关系数,TS,KL
    """
    def __get_data_corr(self,df_1,df_2,move_len):
        #存在数据为nan和inf的，去掉
        
        pd_two = pd.concat([df_1,df_2],axis=1,sort =True)
        pd_two = pd_two.replace([np.inf, -np.inf], np.nan).dropna()
        
        
        item_list_00 = self.__get_best_corr(pd_two,move_len)      #获取最优person平移
        item_list_00 += self.__time_diff_corr_new(pd_two,move_len)    #获取最优TS
        item_list_00 += self.__k_l_info(pd_two,move_len)          #获取最优KL
        #0,3,6位移TS
        for i in [0,3,6]:
            item_list_00 += self.__get_per_ts_kl(pd.concat([df_1,df_2.shift(i)],axis=1,sort=True))
        
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
    def __get_best_corr(self,df,move_len):
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
    def __time_diff_corr_new(self,df,move_len):
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
    def __k_l_info(self,df,move_len):
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
    def __get_per_ts_kl(self,df):
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
    

    """
    生成pd
    """
    def __to_pds(self,str_all_list,data_process):
        str_pd_00 = pd.DataFrame(str_all_list)
        str_pd_00.columns = ["指标1","指标2","最优皮尔逊位移位数","最优位移皮尔逊相关系数",
                            "指标1","指标2","最优TS位移位数","最优TS",
                            "指标1","指标2","最优kl位移位数","最优kl",
                            "未位移皮尔逊相关系数","TS","kl",
                            "位移3个月皮尔逊","位移3个月TS","位移3个月kl",
                            "位移6个月皮尔逊","位移6个月TS","位移6个月kl",
                            "指标1 显著频率top3","指标2 显著频率top3",
                            ]
                       
        
        return str_pd_00

    
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
            #print(pf_all)
            pf_all_cols = pf_all.columns.tolist()
            pf_base = pf_all[pf_all_cols[0]]
            pf_indexs = pf_all[pf_all_cols[1:]]
        elif  index_file_name and  base_file_name:
            pf_base = clean_tool_.data_day2month(base_file_name)
            pf_indexs = clean_tool_.data_day2month(index_file_name)
        else:
            raise("参数错误，文件名不对")
        
        
        pf_all_new=pd.concat([pf_base,pf_indexs],axis=1)
        #pf_all_new= pf_all_new[59:]  #12年后
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
        else:
            raise("data_process  ；只支持 'hp_cycle', 'hp', 'original'3种类型")
        print("data_check",data_check)
        str_all_list=[] 
        print("*"*100)
        print("开始计算相关系数")
        for item in pf_all__new_cols[1:]:
            print("-"*50)
            print("%s  和  %s"%(pf_all__new_cols[0],item))
            item_pf = data_check[item].dropna()
            item_list = self.__get_data_corr(data_check[pf_all__new_cols[0]],item_pf,move_len)
            str_all_list.append(item_list)
        best_pd = self.__to_pds(str_all_list,data_process)  #生成 最优相关系数pd
        time_item = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
        # #加入date，并移到第一列
        # data_check["date"] =data_check.index
        # col_name = data_check.columns.tolist()
        # col_name.insert(0,"date")
        # data_check = data_check.reindex(columns=col_name)
        data_check_name = "%s_%s 原始数据处理后_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item)
        best_pd_name = "%s_%s  最优相关系数_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item)
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
            item_list = self.__get_data_corr(data_check[pf_all__new_cols[0]],item_pf,move_len)
            str_all_list.append(item_list)
        best_pd = self.__to_pds(str_all_list,data_process)  #生成 最优相关系数pd
        time_item = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
        #加入date，并移到第一列
        # data_check["date"] =data_check.index
        # col_name = data_check.columns.tolist()
        # col_name.insert(0,"date")
        # data_check = data_check.reindex(columns=col_name)
        
        data_check.to_csv("%s_%s_原始数据处理后_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item))
        best_pd.to_csv("%s_%s_最优相关系数_%s_%s __%s.csv"%(base_file_name.split(".")[0],
                            index_file_name.split(".")[0],data_process,data_process,time_item))   
        return data_check,best_pd
    
    
    #根据指标的种类，及每种指标占有率选取指标
    def get_best_indexs_by_type(self,list_indexs):
        clean_tool_= clean_tool.Pd_Info()
        pf_type = clean_tool_.get_data_file(self.type_dict_name)

        indexs_type_rate_dict = self.indexs_rate_dict  #各指标比例个数

        indexs_dict = {}      #指标分类
        for index_name in list_indexs:
            for type_i in range(len(pf_type)):
                if index_name == pf_type["col_name"][type_i] or \
                    index_name.split(".")[0] == pf_type["col_name"][type_i] or \
                    index_name.split(".")[0] in pf_type["col_name"][type_i]:
                    if pf_type["type"][type_i] in indexs_dict:
                        indexs_dict[pf_type["type"][type_i]].append(index_name)
                    else:
                        indexs_dict[pf_type["type"][type_i]] = [index_name]
                    break
        
        indexs_list = []  #筛选指标 
        print("指标分类",indexs_dict)
        all_n = 0
        for key  in indexs_type_rate_dict:
            key_n =  indexs_type_rate_dict[key]
            all_n += key_n
            indexs_dict_item =indexs_dict.get(key,[])
            if len(indexs_dict_item):
                indexs_list+= indexs_dict_item[:int(key_n)]
        
        #若指标不够,补充
        if len(indexs_list)< all_n:
            list_key_others = [item for item in indexs_dict.keys() if item not in indexs_type_rate_dict.keys()]
            list_indexs = []
            for item in list_key_others:
                list_indexs += indexs_dict.get(item,[])
            list_add =  [ item for item in list_indexs if item in list_indexs][:all_n-len(indexs_list)]
            
            indexs_list += list_add
            
      
        return indexs_list
        #raise



    
    #获取超前，同步，滞后
    def __get_best_zhibiao(self,pf_corr,pf_all,p,q):
        pf_base = pf_corr # 相关系数
        
        name_lists = ["指标1","指标2","最优TS位移位数","最优TS","最优皮尔逊位移位数","最优位移皮尔逊相关系数"]
        pf_base = pf_base[name_lists]
        #(pf_base['最优皮尔逊位移位数']==pf_base['最优TS位移位数'] )
        
        # best_pf = pf_base[(pf_base['最优位移皮尔逊相关系数']>0.5 )&
                          # #(pf_base['最优TS']>0.5) &
                           # (pf_base['最优皮尔逊位移位数']<12 )& 
                          # (pf_base['最优皮尔逊位移位数']>-12) 
                            # #&(pf_base['最优皮尔逊位移位数']==pf_base['最优TS位移位数'] )                      
                           # ].sort_values(by="最优皮尔逊位移位数",ascending= False)
        
        
        
        best_pf = pf_base[
                        #(pf_base['最优TS']>0.6 ) &
                       (pf_base['最优TS位移位数']<10 )& 
                      (pf_base['最优TS位移位数']>-10) 
                       #&(pf_base['最优皮尔逊位移位数']==pf_base['最优TS位移位数'] ) 
                       ].sort_values(by="最优TS",ascending= False)
          
        print("!"*100,"最优相关系数排序")
        print(best_pf)
        move_name = "最优TS位移位数"
        pf_check = best_pf[move_name]
        list_1_ts = best_pf[(pf_check<q)& (pf_check>p)]
        list_2_ts = best_pf[(pf_check<=p )& (pf_check>=-p)]
        list_3_ts =  best_pf[(pf_check<-p )& (pf_check>-q)]
        print("最优超前指标",list_1_ts)
        list_1_ts.to_csv("最优超前指标.csv")
        list_1 = list_1_ts["指标2"].tolist()[10:20]
        #按照比例获取各种分类的数据
        
        list_1 = self.get_best_indexs_by_type(list_1_ts["指标2"].tolist())
        #######################################################
        # #自己设定超前指标
        list_5 = [
                # "商品房销售面积:办公楼:累计同比",
                # "人民币:各项贷款余额:境内贷款:住户贷款.2_同比(12个月)",
                # "OECD综合领先指标:中国.2_同比(12个月)",
                # "汽车制造:应收票据及应收账款:同比",
                # "平均汇率:欧元兑人民币.2_同比(12个月)",
                # "人民币:各项存款余额:境内存款:住户存款:活期存款",
                # "产量:发动机:当月同比",
                # "债券型基金总数.2_同比(12个月)",
                # "人民币:各项存款余额:境内存款:非金融企业存款",
                # "M2",
                # "产量:载货汽车:当月同比",
                # "产量:商用车:柴油汽车:当月同比",
                # "CPI:服务:当月同比",
                # "销量:商用车:柴油汽车:当月同比",
                # "产量:商用车:货车非完整车辆:当月同比",
                # "PMI:进口",
                # "产量:平板玻璃:当月同比",
                # "产量:商用车:货车:当月同比",
                
                
                # #TEMPLE2
                # "PMI:进口",
                # "CPI:服务:当月同比",
                # "上海私车牌照拍卖:平均中标价",
                # "SITC:出口金额:当月值:67章 钢铁",
                # "销量:汽车:国内制造:当月值",
                # "商品房销售面积:办公楼:累计同比",
                # "上海私车牌照拍卖:投放数量",
                # "OECD综合领先指标:幅度调节型:中国.2_同比(12个月)",
                # "产量:载货汽车:当月同比",
                # "M2",
                # "产量:商用车:柴油汽车:当月同比",
                # #"销量:商用车:柴油汽车:当月同比",
                # "产量:商用车:货车非完整车辆:当月同比",
                # "汽车制造:应收票据及应收账款:同比",
                # "人民币:各项存款余额:境内存款:住户存款:活期存款",
                # #"平均汇率:欧元兑人民币.2_同比(12个月)",
                # "产量:发动机:当月同比",
                
                #temple3
                # "SITC:贸易差额:当月值:67章 钢铁",
                # "HS:贸易差额:累计值:72章 钢铁",
                # "农业生产资料价格指数:农用手工具:累计同比",
                # "运输设备及生产用计数仪表制造:财务费用:累计同比",
                # "齿轮及齿轮减、变速箱制造:产成品存货",
                # #"出口数量:钢铁板材:累计同比",
                
                # "商品房销售面积:办公楼:累计同比",
                # "人民币:各项贷款余额:境内贷款:住户贷款.2_同比(12个月)",
                # "OECD综合领先指标:幅度调节型:中国.2_同比(12个月)",
                # "汽车制造:应收票据及应收账款:同比",
                # # "平均汇率:欧元兑人民币.2_同比(12个月)",
                # "人民币:各项存款余额:境内存款:住户存款:活期存款",
                # "产量:发动机:当月同比",
                # # # "OECD综合领先指标:幅度调节型:四个主要欧洲国家.2_同比(12个月)",
                # # # "OECD综合领先指标:四个主要欧洲国家.2_同比(12个月)",
                # # "债券型基金总数.2_同比(12个月)",
                # # # "OECD综合领先指标:幅度调节型:五个主要亚洲国家.2_同比(12个月)",
                # # "人民币:各项存款余额:境内存款:非金融企业存款",
                # # "M2",
                # "产量:载货汽车:当月同比",
                # # "人民币:各项存款余额:境内存款:非金融企业存款:活期存款",

                
                #temple4
                "HS:贸易差额:累计值:72章 钢铁",
                "进口金额:钢铁管材及空心异形材:累计值",
                "土地购置费:累计同比",
                "出口金额:钢铁板材:当月值",
                "进口数量:小客车(九座及以下的)(包括整套散件):累计值",
                "SITC:出口金额:当月值:67章 钢铁",
                "商品房销售面积:累计同比",
                "HS:出口金额:累计值:72章 钢铁",
                "SITC:贸易差额:累计值:67章 钢铁",
                "商品房销售面积:办公楼:累计同比"
                
                
                ]
        # list_1 =sample(list_1,8)
        #######################################################
        if "货币当局:债券发行.2同比(12个月)" in list_1:
            list_1.remove("货币当局:债券发行.2同比(12个月)")
        # if "金融机构:人民币:黄金占款" in list_1:
            # list_1.remove("金融机构:人民币:黄金占款")
        list_2 = list_2_ts["指标2"].tolist()[:10]
        list_2 = list_2
        list_3 = list_3_ts["指标2"].tolist()[:10]
        
        all_name_list = [list_1,list_2,list_3]  #取出的名称
        
        #TS排序，若TS位移为正，person为负，翻转该数据
        #若TS位移为负，person为正，翻转该数据
        #若一个为0，一个为12，翻转
        for item in list_1+list_2+list_3:
            index_1 = pf_base[(pf_base['指标2']==item )]["最优TS位移位数"].tolist()[0]
            index_2 = pf_base[(pf_base['指标2']==item )]["最优皮尔逊位移位数"].tolist()[0]
            # if  (index_1> 0 and  index_2< 0 ) or \
                # (index_1 == 0 and  index_2 == 12) :
            if  index_1!= index_2:
                print("TS位移与person位移不一致，翻转该数据",item) 
                pf_all[item]=-pf_all[item]
                 
            
        best_df_list = [pf_all[item].dropna() for item in all_name_list] #对应最优的数据
        
        return best_df_list
    
    #标准化变化率
    def __get_std_rate(self,df):
        df = df.dropna()
        A = abs(df).sum()/len(df)
        return df/A

    #权重比率RT    
    def __get_R(self,df,corr_list = []):
        W1 = np.ones(df.shape[1]) #当前为等权重
        RT = ""
        RT1 = (df*W1).sum(axis=1)/np.sum(W1)
        
        if len(corr_list) == df.shape[1]:
            W = np.array(corr_list)
            RT = (df*W).sum(axis=1)/np.sum(W)
        
        print ("-----------------RT",RT)
        print ("=================RT1",RT1)
        if len(RT):
            return RT
        else:
            return RT1
        
    #获取对称变换率
    def __get_Symmetric_rate(self,df):
        
        if not isinstance(df, pd.Series):
            print("传入数据类型错误！！")
            raise 
        #非比率序列，100左右数据
        c = ""
        if 0<df.min()<100 and df.max()>100:
            c = 200*(df -df.shift(1))/(df +df.shift(1))
        else:
            c=df.diff(1)
        Std_c = self.__get_std_rate(c)
        #print("0000000",abs(Std_c).sum()/len(Std_c))
        return Std_c

    #求初始合成指数    
    def __get_init_ci(self,df):
        if not isinstance(df, pd.Series):
            print("传入数据类型错误！！")
            raise 
        I = 100
        I_list = [I]
        for item in df:
            I = I*(200+item)/(200-item)
            I_list.append(I)
        I1 = pd.Series(I_list)
        I2 = I1.sum()/(100*len(I1))
        ci_init =(I1/I2)
        return ci_init
        
           
    """
    參数：
        - XMat：传入的是一个numpy的矩阵格式，行表示样本数，列表示特征    
        - k：表示取前k个特征值相应的特征向量
    返回值：
        - finalData：參数一指的是返回的低维矩阵，相应于输入參数二
        - reconData：參数二相应的是移动坐标轴后的矩阵
    """
    def pca(self,XMat, k):
        XMat_new= XMat
        data_adjust = np.mat(XMat_new).T  #创建矩阵，并转置
        # 求均值
        mean_matrix = np.mean(data_adjust, axis=1)
        data_adjust = data_adjust - mean_matrix
        n = len(data_adjust) #原始维度
        covX = np.cov(data_adjust,rowvar=True)   #计算协方差矩阵 rowvar:默认为True,此时每一行代表一个变量（属性），每一列代表一个观测；为False时，则反之

        featValue, featVec=  np.linalg.eig(covX)  #求解协方差矩阵的特征值和特征向量
        #print("covX", covX,featValue,featVec)
        index = np.argsort(-featValue) #依照featValue进行从大到小排序
        finalData = []
        if k > n:
            print ("k must lower than feature number")
            return
        else:
            #注意特征向量是列向量。而numpy的二维矩阵(数组)a[m][n]中，a[1]表示第1行值
            selectVec = featVec.T[index[k-1:k]] #所以这里须要进行转置 ,按照排列取特征向量
            finalData = selectVec*data_adjust #提取主成分
            #成分贡献率为：
            v_con = featValue[index[k-1]]/sum(featValue)
            #print("v_con",v_con)
            finalData=pd.DataFrame(finalData.T,XMat.index,columns=["PCA  第%s成分贡献率为：%s"%(k,v_con)])
        return finalData        
        
        
    #ci合成指数    df1超前 ,df2同步，df3滞后
    def __get_ci(self,list_df):
        rjt_list = []  
        i=0             
        for df in list_df:
            #print("666666666",df)
            df = df.apply(lambda x: (x - np.mean(x)) / (np.std(x))) #Z-score标准化方法
            #df = df.rolling(window=3).mean().dropna()  #移动平均
            #PCA合成
            # pca=PCA(n_components=1)
            # print(pca.fit_transform(df))
            # pca_df = pd.DataFrame(pca.fit_transform(df),df.index)
            # print(pca_df)
            # pca_df = self.pca(df,1)
            title_list = ["超前指标","同步指标","滞后指标"]
            
            df.to_csv("%s_合成数据.csv"%title_list[i])
            df.plot(title=title_list[i])
            
            st = df.apply(self.__get_Symmetric_rate)
            RT = self.__get_R(st)
            i+=1
            rjt_list.append(RT)
            
        f1 =  abs(rjt_list[0]).sum()/ abs(rjt_list[1]).sum()
        f2 = 1
        f3 = abs(rjt_list[2]).sum()/ abs(rjt_list[1]).sum()
        #标准化因子
        f_list = [f1,f2,f3]
        vjt_pf = pd.concat(rjt_list,axis=1)/np.array(f_list)
        init_pf = vjt_pf.apply(self.__get_init_ci)

        return init_pf



    #判断DI 1,0,0.5
    def __di_data_check(self,df):
        new_list =[]
        for item in df:
            new_item =""
            if item<0.01 and item>-0.01:
                new_item = 0.5
            elif item >0.01:
                new_item = 1
            elif item <-0.01:
                new_item = 0
            new_list.append(new_item)
        return pd.Series(new_list,df.index)
        
    #DI合成指数    df1超前 ,df2同步，df3滞后
    def __get_DI(self,list_df):
        di_list = []  
        for df in list_df:
            
            df_shift=df.copy().shift(3)
            df_I = ((df - df_shift)/abs(df)).dropna()
            df_check = df_I.apply(self.__di_data_check)
            df_di = df_check.sum(axis=1)/df.shape[1]
            df_di_roll = df_di.rolling(window=5).mean().shift(-2)  #移动平均5个月
            di_list.append(df_di_roll)
            
            # #画DI图
            # pf_di_all = pd.concat([df_di,df_di_roll],axis=1)
            # pf_di_all.plot()
            # plt.show()
        DI_PF = pd.concat(di_list,axis=1) 
        DI_PF.name = "DI合成指数"    
        DI_PF.columns = ["超前","一致","滞后"]
        return DI_PF
            
    
    
    #输入预测序列同比序列， 指标原始序列，根据预测序列推出同比序列，得到原始序列
    def zhibiao_res(self,pf,original_name,time_item):
        cols = pf.columns.tolist()
        a,b,best_corr_step,best_corr = self.__get_best_corr(pf,8) #12个月内的的数据进行TS
        
        #best_corr_step=-8
        #根据两者比例进行换算
        pd_hecheng = pf[cols[0]][best_corr_step-1:]
        pd_hecheng_rate = (pf[cols[0]][best_corr_step:] -pf[cols[0]][best_corr_step-1])/abs(pf[cols[1]][-1])
        print("pd_hecheng",pd_hecheng)
        print("pd_hecheng_rate",pd_hecheng_rate)
        #pd_pridict  = [ i*pf[cols[1]][-1]/pd_hecheng[best_corr_step-1] for i in pd_hecheng[best_corr_step:]]
        pd_pridict  = [(i+1)*pf[cols[1]][-1] for i in pd_hecheng_rate]
        print("pd_pridict",pd_pridict)
        print("best_corr_step",pf[cols[1]][-1])
        list_tb =  pf[cols[1]].tolist()+pd_pridict
        
        tb_pd = pd.Series(list_tb,index = pd.date_range(start = pf.index[0],periods = len(list_tb),freq="M"))
        tb_pd.index = tb_pd.index.map(lambda x: x.strftime('%Y-%m'))
        tb_pd.name = "%s_预测"%cols[1]
        
        #根据原始序列进行还原
        if original_name:
            clean_tool_= clean_tool.Pd_Info()
            pf_or = clean_tool_.data_day2month(original_name)
            pf_all = pd.concat([tb_pd,pf_or],axis =1,sort=True) 
            cols = pf_all.columns.tolist()
            print(pf_all)
            pf_all["%s_预测"%cols[1]] = pf_all[cols[1]].shift(12)*(1+ pf_all[cols[0]]/100)
            print(pf_all)
            
            return pf_all
            
        return pd.concat([pf,tb_pd],axis=1,sort=True)
    
    """
    获取CI_DI:
    参数：p,q
    
    return 
    """
    def main_CI_DI(self,p,q,data_check_name="",best_pd_name="",original_name =""):
        clean_tool_= clean_tool.Pd_Info()
        if len(data_check_name) and len(best_pd_name):
            pf_base = clean_tool_.data_day2month(data_check_name)
            best_pd = clean_tool_.get_data_file(best_pd_name)
        
            pf_cols = pf_base.columns.tolist()
            best_name_df_list = self.__get_best_zhibiao(best_pd,pf_base,p,q) #最优的相关数据名字

            init_pfs = self.__get_ci(best_name_df_list)  #获取CI
            DI_PF = self.__get_DI(best_name_df_list)    #获取DI
            
            DI_PF.plot(title = DI_PF.name)
            
            init_pfs.index = pf_base.index[len(pf_base)-len(init_pfs):]      
            pfs_all = pd.concat([init_pfs,pf_base[pf_cols[0]]],axis=1)
            
            #pfs_all = pfs_all.apply(self.hp_lb_c)
            name_list = ["超前","一致","滞后",pfs_all.columns.tolist()[3]]
            pfs_all.columns = name_list
            pfs_all = pfs_all[ [pfs_all.columns.tolist()[0], pfs_all.columns.tolist()[-1]]] #挑选指标
            time_item = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
            pfs_all = self.zhibiao_res(pfs_all,original_name,time_item)
            
            cols = pfs_all.columns.tolist()
            print("pfs_all",pfs_all)
            #pfs_all = pfs_all.rolling(window=2).mean().dropna()  #移动平均2个月
            ax = pfs_all.plot(use_index=True, y=cols, figsize=(10, 6),
                                secondary_y=cols[-2:-1], title="CI指标对比(%s)"%data_check_name)
            
            
            file_name = "合成超前_%s_%s.csv"%(data_check_name,time_item)
            pfs_all["date"] = pfs_all.index
            pfs_all.to_csv(file_name,index =False)
            plt.show()
 


 