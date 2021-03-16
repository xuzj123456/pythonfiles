import data_cycle_lib.data_clean_lib as  clean_tool
import matplotlib.pyplot as plt
import  data_cycle_lib.best_corr_CI_DI as  CCD
import pandas as pd

clean_tool_= clean_tool.Pd_Info()

#将设定的基准数据提前到第一列
def set_base(base_name,pd_all):
    cols = list(pd_all)
    cols.insert(0,cols.pop(cols.index(base_name)))
    pf_res = pd_all.loc[:,cols]
    #pf_res = pf_res.rolling(window=3,center=True,min_periods=2).mean().dropna()  #中心移动平均3个月
     
    return pf_res


#相关性  
def best_corr_main():
    ccd = CCD.CI_AND_DI()  #获取指标分类数据
    
    base_file_name = r"E:\微信\新建文件夹\WeChat Files\xisijialouluo\FileStorage\File\2019-12\X13_房地产数据 (2)_2019-12-04 09-49-13.xlsx"
    pf_base = clean_tool_.data_day2month(base_file_name)
    
    
    base_name = '商品房销售额:累计值'
    pf_all = set_base(base_name,pf_base)
    pf_all["date"] = pf_all.index
    
    #按照时间截取：
    time_cut =''
    pf_all = pf_all.truncate(before =time_cut )

    #基准移动平均
    #pf_all[base_name] = pf_all[base_name].rolling(window=3,center=True,min_periods=2).mean().dropna()  #中心移动平均3个月
   
    
    file_all_name = "%sand%s_%s.xlsx"%(base_file_name.split(".")[0],
                        base_name.replace(":","_"),time_cut)
                        
    pf_all.to_excel(file_all_name,index =False)
    
    
    
    """
    基准序列在第一列
    日期列名为date
    move_len ： 多少范围内位移，默认：12 
    data_process:  "original" 为原始数据,    "hp" 原始数据进行hp处理后的周期项数据
    """
    ccd.get_best_corr_data(file_all_name,move_len=12,data_process ="hp")  #获取周期数据及最优相关系数

if __name__ == "__main__":   
    best_corr_main()
