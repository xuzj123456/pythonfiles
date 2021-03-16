#-*- coding:utf-8 -*-
import  data_cycle_lib.best_corr_CI_DI as  CCD
import os

file = '宏观数据_基础.xlsx'

    
if __name__=="__main__":
    ccd = CCD.CI_AND_DI() 
     #获取最优相关系数
    ccd.get_best_corr_data(file,
                        move_len=12,data_process ="") 
    
    