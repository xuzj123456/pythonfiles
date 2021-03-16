#-*- coding:utf-8 -*-

from pandas import read_excel 
from pandas import read_csv 
from pandas import to_datetime 
import sys,re
import rpy2.robjects as robjects
import time,os
import traceback



robjects.r('''
           f <- function(){
           library(plm)
            #library(MSBVAR)
            library(tseries)
            library(xts)
            library(mice)
            library(foreign)
            library(Hmisc)
            library(factoextra)
            library(vars)
            library(urca)
            library(xtable)
            library(flextable)
            library(panelvar)
            library(seasonal)
            library(FNN)
            library(plotrix)
            library(TTR)
            library(lubridate)
            library(signal)
           }
           ''')



#R代码
robjects.r('''data_clean_x13 <-  function(name, time_start,plot = TRUE){
              data(seasonal)
              data(holiday)  
              guoqing = c(as.Date("2008-09-29"),as.Date("2009-10-01"),as.Date("2010-10-01"),
                          as.Date("2011-10-01"),as.Date("2012-09-30"), as.Date("2013-10-01"),
                          as.Date("2014-10-01"),as.Date("2015-10-01"),as.Date("2016-10-01"), 
                          as.Date("2017-10-01"),as.Date("2018-10-01"),as.Date("2019-10-01"),
                          as.Date("2020-10-01"),as.Date("2021-10-01"),as.Date("2022-10-01"),
                          as.Date("2023-10-01"),as.Date("2024-10-01"),as.Date("2025-10-01"))

              ch_holiday = cny

              for(i in 1:length(cny)){
                for(k in 1: length(guoqing)){
                   if(year(cny[i]) == year(guoqing[k])){
                      ch_holiday = append(ch_holiday, guoqing[k], after = (i+k-1))
                      break
                   }
                }
              }

          obj = read.csv(name, header = FALSE, fileEncoding = 'utf-8')
          #obj = obj[,-c(162,419,442,459,710)]
          fix_data = obj
          adj_data = obj
          ch_hday = list(holiday = ch_holiday, chunjie = cny)
          
          nas = colnames(obj)
          #cat(nas)
          #节日设置
          chny = genhol(ch_hday$chunjie, start=0, end=6, center="calendar")

          if(plot == TRUE){
            for (i in 2:dim(obj)[2]){
              cat("-------", "\n")
              cat(i, nas[i], "\n")
              sh = (obj[,i])
              #cat("2222222222222222")
              #cat(sh)
              #除去负数效果
              if(min(sh) <= 0){
                sh = sh + abs(min(sh))+ 0.00001
              }
              sh_seas = {}
              s1 = ts(sh, frequency = 12, start = time_start) # 需要调整起始日期
              sh_seas = tryCatch({seas(s1, xreg=chny, regression.usertype="holiday", outlier = NULL)},
                              error=function(e) { print(e)})
              # print(sh_seas)
              # print(sh_seas$data)
              #sh_seas = seas(s1, x11="")
              if (class(sh_seas)=="seas"){
                  plot(sh_seas)
                  title(i)
                  fix_data[,i] = sh_seas$data[,1]
                  #adj_data[,i] = sh_seas$data[,5]
                  
              }
            }
          }else{
            for (i in 2:dim(obj)[2]){

              sh = (obj[,i])
              cat("-------", "\n")
              cat(i, nas[i], "\n")

              #除去负数效果
              if(min(as.numeric(sh)) < 0){

                sh = sh + abs(min(sh))+0.0000001
              }

              s1 = ts(sh, frequency = 12, start = time_start) # 需要调整起始日期
              sh_seas = tryCatch({seas(s1, xreg=chny, regression.usertype="holiday", outlier = NULL)},
                              error=function(e) { print(e)})
               if (class(sh_seas)=="seas"){
              fix_data[,i] = sh_seas$data[,1]
              #adj_data[,i] = sh_seas$data[,5]
              }
            }

          }

          return(list(data = fix_data, adjust = adj_data ))
        }'''
      )
      



def data_day2month( file_name,flag="last"):
        
        if re.search("xls",file_name,re.I):
            df = read_excel(file_name)
        elif  re.search("csv$",file_name,re.I):
            df = read_csv(file_name)
        else:
            raise("数据文件格式错误，需要为csv、xls、xlsx！！")
        df = df.dropna(axis=1,how='all')  # 去除空列
        # 将天换成月
        if "date" in df.columns.tolist():
            df['date'] = to_datetime(df['date'])
            df['date'] = df['date'].map(lambda x: x.strftime('%Y-%m'))
            df_ = df.drop_duplicates('date', flag)
            df_= df_.set_index(["date"])

            return df_
        else:
            raise("数据  日期列名需要为date ！！")


def get_x13(*args):
    file_name,start_year,start_month = args 
    print("*"*100)
    print("="*50)
    print("开始处理：file_name: %s,start_year: %s ,start_month: %s"%(file_name,start_year,start_month))
    pf_index = data_day2month(file_name)
    time_item = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
    no_head_csv_name = "no_header_%s_%s.csv"%(file_name.split(".")[0],time_item)
    
    start_month =str(int(start_month))
    #截取日期之后
    pf_index.truncate(before = "%s-%s"%(start_year,start_month.zfill(2))).to_csv(no_head_csv_name,header=False)
    
    
    #R进行X13处理
    print("="*50)    
    print("加载R库")
    robjects.r['f']()
    print("="*50)
    print("开始X13处理")
    time_start = robjects.r['c'](eval(start_year),eval(start_month))
    x13_no_header_csv_name = ""
    try:
        list_data = robjects.r['data_clean_x13'](no_head_csv_name, time_start,plot=False)
        df_R = list_data[0]  #R类型DataFrame,需要R中数据进行保存
        x13_no_header_csv_name = "X13_%s.csv"%(no_head_csv_name.split(".")[0])
        df_R.to_csvfile(x13_no_header_csv_name,row_names=False,eol="\n")
    except :
        print("!"*100)
        print("X13处理错误，请检查数据列中是否存在空值！！！")
        print("错误信息为：%s"%(str(traceback.format_exc())))
        print("!"*100)
    finally:
        os.remove(no_head_csv_name)  #删除没有header的原始数据 
        
    if x13_no_header_csv_name:
        pf_end = read_csv(x13_no_header_csv_name)
        pf_end.columns = ["date"]+pf_index.columns.tolist()
        print("="*50)    
        print("添加列名")
        end_file_name = "X13_%s_%s.csv"%(file_name.split(".")[0],time_item)
        pf_end.to_csv(end_file_name,index =False)
        print("="*50)   
        os.remove(x13_no_header_csv_name)  #删除没有header的X13数据 
        print("X13处理完成：file_name: %s"%end_file_name)
        
        print("*"*100)
        return end_file_name
            
# 输入参数
# name = "宏观月频_填充.xlsx"
# pf_index = data_day2month(name)
# print(pf_index)
# pf_all = pf_index.truncate(before = "%s-%s"%("2008","2".zfill(2)))
# for i in range(0,len(pf_all),6):
    # if i+89 <=len(pf_all):
        # pf_cut = pf_all[i:i+89]
        # print(pf_cut)
        # cut_name = "%s_%s_%s.xlsx"%(name.split(".")[0],pf_cut.index[0],pf_cut.index[-1])
        # pf_cut.to_excel(cut_name)
        # get_x13(cut_name,pf_cut.index[0].split("-")[0],pf_cut.index[0].split("-")[1])
        
        
    