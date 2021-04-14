# -*- coding: utf-8 -*-
#import math
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
#coef, p = spearmanr(data1, data2)
import statsmodels.api as sm
#res = sm.RLM(y, x).fit()
#res.pvalues
#res.params
#from sklearn import preprocessing

binret=pd.read_excel("原始数据.xlsx",sheet_name='基准指数').iloc[1:,2]
#rdata=pd.read_excel("C:/Users/dell/Desktop/中信实习/食品饮料/分股票/区间收益率.xlsx")
rdata=pd.read_excel("区间收益率.xlsx",sheet_name='延后二个月')
inlist=['对数营收','预收账款于营收占比','预收账款同比增速','应收账款周转率','存货周转率','销售费用率','销售毛利率同比',
        'ROE','净利润增长率','营业收入增长率','归母净利润增长率','经营净现金流同比']
alpha=0.05#显著性水平

def rofit(index):#输入指标名称，返回图表1的7个值
    data=pd.read_excel("原始数据.xlsx",sheet_name=index)
    noterm=len(rdata.columns[2:])
    apar=[]#全部的系数
    apva=[]#全部的P值
    nopos=0#正向显著系数个数
    noneg=0#反向显著系数个数
    notx=0#同向显著次数
    nofx=0#反向显著次数
    spn=0
    fx=' '
    for i in range(noterm):
        mid=pd.concat([data['证券简称'],rdata.iloc[:,i+2],data.iloc[:,i+4]],axis=1)
        mid=mid[~mid['证券简称'].str.contains("ST")].dropna()
        #res=sm.RLM(preprocessing.minmax_scale(np.power(1+mid.iloc[:,1]/100,1/3)-1, feature_range=(-1, 1)),sm.add_constant(preprocessing.minmax_scale(mid.iloc[:,2], feature_range=(-1, 1)))).fit()
        res=sm.RLM(100*(np.power(mid.iloc[:,1]/100+1,1/3)-1),mid.iloc[:,2]).fit()
        apar.append(float(res.params))
        apva.append(float(res.pvalues))
        if float(res.pvalues)<alpha:
           if float(res.params)*spn>0:
              notx+=1
           else:
              nofx+=1
           spn=float(res.params)
           if float(res.params)<0:
              noneg+=1
           else:
              nopos+=1
    if nopos>noneg:
       fx='+'
    elif noneg>nopos:
       fx='-'
    return apar,apva,nopos/noterm,noneg/noterm,notx/noterm,nofx/noterm,fx,abs(nopos-noneg)/noterm,(notx-nofx)/noterm

'''
输出表1数据和全部系数
'''   
chart1=pd.DataFrame(index=inlist,columns=['正相关显著比例','负相关显著比例','同向显著次数占比',
                                          '状态切换次数占比','显著比例较高的方向','abs(正-负)','同向-切换'])

ancha1=pd.DataFrame(columns=['数据类别','201001','201002','201003','201004','201101','201102',
                             '201103','201104','201201','201202','201203','201204','201301','201302',
                             '201303','201304','201401','201402','201403','201404','201501','201502','201503',
                             '201504','201601','201602','201603','201604','201701','201702','201703','201704',
                             '201801','201802','201803','201804','201901','201902','201903','201904'],
                    index=['对数营收','对数营收','预收账款于营收占比','预收账款于营收占比','预收账款同比增速',
                           '预收账款同比增速','应收账款周转率','应收账款周转率','存货周转率','存货周转率',
                           '销售费用率','销售费用率','销售毛利率同比','销售毛利率同比','ROE','ROE',
                           '净利润增长率','净利润增长率','营业收入增长率','营业收入增长率','归母净利润增长率',
                           '归母净利润增长率','经营净现金流同比','经营净现金流同比'])
ancha1['数据类别']=('回归系数','p值','回归系数','p值','回归系数','p值','回归系数','p值','回归系数','p值',
                   '回归系数','p值','回归系数','p值','回归系数','p值','回归系数','p值','回归系数','p值',
                   '回归系数','p值','回归系数','p值')

for i in range(len(inlist)):#填表1
    mid=rofit(inlist[i])
    chart1.loc[inlist[i]]=mid[2:]
    ancha1.iloc[2*i,1:]=tuple(mid[0])
    ancha1.iloc[2*i+1,1:]=tuple(mid[1])
    

      
def rcoef(index):#输入指标名称，返回图表2的7个值
    data=pd.read_excel("原始数据.xlsx",sheet_name=index)
    noterm=len(rdata.columns[2:])
    apar=[]#全部的系数
    apva=[]#全部的P值
    nopos=0#正向显著系数个数
    noneg=0#反向显著系数个数
    notx=0#同向显著次数
    nofx=0#反向显著次数
    spn=0
    fx=' '
    for i in range(noterm):
        mid=pd.concat([data['证券简称'],rdata.iloc[:,i+2],data.iloc[:,i+4]],axis=1)
        mid=mid[~mid['证券简称'].str.contains("ST")].dropna()
        #coef, p = spearmanr(data1, data2)
        coef, p = spearmanr(100*(np.power(mid.iloc[:,1]/100+1,1/3)-1),mid.iloc[:,2])
        apar.append(coef)
        apva.append(p)
        if p<alpha:
           if coef*spn>0:
              notx+=1
           else:
              nofx+=1
           spn=coef
           if coef<0:
              noneg+=1
           else:
              nopos+=1
    if nopos>noneg:
       fx='+'
    elif noneg>nopos:
       fx='-'
    return apar,apva,nopos/noterm,noneg/noterm,notx/noterm,nofx/noterm,fx,abs(nopos-noneg)/noterm,(notx-nofx)/noterm

'''
输出表2数据和全部系数
'''   
chart2=pd.DataFrame(index=inlist,columns=['正相关显著比例','负相关显著比例','同向显著次数占比','状态切换次数占比',
                                          '显著比例较高的方向','abs(正-负)','同向-切换'])

ancha2=pd.DataFrame(columns=['数据类别','201001','201002','201003','201004','201101','201102',
                             '201103','201104','201201','201202','201203','201204','201301','201302',
                             '201303','201304','201401','201402','201403','201404','201501','201502','201503',
                             '201504','201601','201602','201603','201604','201701','201702','201703','201704',
                             '201801','201802','201803','201804','201901','201902','201903','201904'],
                    index=['对数营收','对数营收','预收账款于营收占比','预收账款于营收占比','预收账款同比增速',
                           '预收账款同比增速','应收账款周转率','应收账款周转率','存货周转率','存货周转率',
                           '销售费用率','销售费用率','销售毛利率同比','销售毛利率同比','ROE','ROE',
                           '净利润增长率','净利润增长率','营业收入增长率','营业收入增长率','归母净利润增长率',
                           '归母净利润增长率','经营净现金流同比','经营净现金流同比'])
ancha2['数据类别']=('秩相关系数','p值','秩相关系数','p值','秩相关系数','p值','秩相关系数','p值','秩相关系数','p值',
                   '秩相关系数','p值','秩相关系数','p值','秩相关系数','p值','秩相关系数','p值','秩相关系数','p值',
                   '秩相关系数','p值','秩相关系数','p值')

for i in range(len(inlist)):#填表2
    mid=rcoef(inlist[i])
    chart2.loc[inlist[i]]=mid[2:]
    ancha2.iloc[2*i,1:]=tuple(mid[0])
    ancha2.iloc[2*i+1,1:]=tuple(mid[1])    
    
    
def groups(index, ind):#输入数据和行业，输出5组的收益序列
    r1=[]#存放收益率序列
    r2=[]
    r3=[]
    r4=[]
    r5=[]
    sar1=pd.DataFrame()#存放收益率和股票名称序列
    sar2=pd.DataFrame()
    sar3=pd.DataFrame()
    sar4=pd.DataFrame()
    sar5=pd.DataFrame()
    
    data=pd.read_excel("原始数据.xlsx",sheet_name=index)
    if ind=='行业':
       pass          
    else:
       data=data[data['二级分类']==ind]

    for i in range(len(data.columns[4:])):
        mid=pd.concat([data['证券简称'],rdata.iloc[:,i+2],data.iloc[:,i+4]],axis=1).dropna()#三列：名字，收益率，指标值
        mid=mid[~mid['证券简称'].str.contains("ST")]#删除ST
        mid=mid.sort_values(by=mid.columns[2],ascending=False).reset_index(drop=True)
        ret1=mid.iloc[:int(len(mid)/5),:2].reset_index(drop=True)
        ret2=mid.iloc[int(len(mid)/5):2*int(len(mid)/5),:2].reset_index(drop=True)
        ret3=mid.iloc[2*int(len(mid)/5):3*int(len(mid)/5),:2].reset_index(drop=True)
        ret4=mid.iloc[3*int(len(mid)/5):4*int(len(mid)/5),:2].reset_index(drop=True)
        ret5=mid.iloc[4*int(len(mid)/5):,:2].reset_index(drop=True)
        sar1=pd.concat([sar1,ret1],axis=1)
        sar2=pd.concat([sar2,ret2],axis=1)
        sar3=pd.concat([sar3,ret3],axis=1)
        sar4=pd.concat([sar4,ret4],axis=1)
        sar5=pd.concat([sar5,ret5],axis=1)
        r1.append(np.mean(ret1.iloc[:,1])-binret.iloc[i])
        r2.append(np.mean(ret2.iloc[:,1])-binret.iloc[i])
        r3.append(np.mean(ret3.iloc[:,1])-binret.iloc[i])
        r4.append(np.mean(ret4.iloc[:,1])-binret.iloc[i])	
        r5.append(np.mean(ret5.iloc[:,1])-binret.iloc[i])
    
    c=pd.concat([pd.DataFrame(r1).T,pd.DataFrame(r2).T,pd.DataFrame(r3).T,pd.DataFrame(r4).T,pd.DataFrame(r5).T])
    sar1=pd.concat([pd.DataFrame(columns=['不同行业','组别'],index=list(range(len(sar1)))),sar1],axis=1)
    sar1['组别']='第一组'
    sar2=pd.concat([pd.DataFrame(columns=['不同行业','组别'],index=list(range(len(sar2)))),sar2],axis=1)
    sar2['组别']='第二组'
    sar3=pd.concat([pd.DataFrame(columns=['不同行业','组别'],index=list(range(len(sar3)))),sar3],axis=1)
    sar3['组别']='第三组'
    sar4=pd.concat([pd.DataFrame(columns=['不同行业','组别'],index=list(range(len(sar4)))),sar4],axis=1)
    sar4['组别']='第四组'
    sar5=pd.concat([pd.DataFrame(columns=['不同行业','组别'],index=list(range(len(sar5)))),sar5],axis=1)
    sar5['组别']='第五组'
    d=pd.concat([sar1,sar2,sar3,sar4,sar5])
    d['不同行业']=ind
    return c,d


chart3=pd.DataFrame(columns=['分组方法','第一组年化超额收益','第一组信息比率','第五组年化超额收益','第五组信息比率',
                             '第一组和第五组之差的绝对值'],index=['对数营收','对数营收','对数营收','对数营收',
                            '预收账款于营收占比','预收账款于营收占比','预收账款于营收占比','预收账款于营收占比',
                            '预收账款同比增速','预收账款同比增速','预收账款同比增速','预收账款同比增速','应收账款周转率',
                            '应收账款周转率','应收账款周转率','应收账款周转率','存货周转率','存货周转率','存货周转率',
                            '存货周转率','销售费用率','销售费用率','销售费用率','销售费用率','销售毛利率同比',
                            '销售毛利率同比','销售毛利率同比','销售毛利率同比','ROE','ROE','ROE','ROE','净利润增长率',
                            '净利润增长率','净利润增长率','净利润增长率','营业收入增长率','营业收入增长率',
                            '营业收入增长率','营业收入增长率','归母净利润增长率','归母净利润增长率','归母净利润增长率',
                            '归母净利润增长率','经营净现金流同比','经营净现金流同比','经营净现金流同比',
                            '经营净现金流同比'])
    
chart3['分组方法']=('行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类',
      '食品','饮料','行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类',
      '食品','饮料','行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类','食品','饮料','行业','酒类',
      '食品','饮料')

glist=['行业','酒类','食品','饮料']

for i in range(len(inlist)):#填表3
    for j in range(len(glist)):
        if glist[j]=='行业':
           data=pd.read_excel("原始数据.xlsx",sheet_name=inlist[i])
           mid=groups(inlist[i], glist[j])[0]
        else:
           data=pd.read_excel("原始数据.xlsx",sheet_name=inlist[i])
           data=data[data['二级分类']==glist[j]]
           mid=groups(inlist[i], glist[j])[0]
        
        ret1=np.power((mid.iloc[0,:]+1).prod(),0.1)-1
        std1=np.std(mid.iloc[0,:])*2
        ret5=np.power((mid.iloc[4,:]+1).prod(),0.1)-1
        std5=np.std(mid.iloc[4,:])*2
        chart3.iloc[4*i+j,1:]=(ret1,ret1/std1,ret5,ret5/std5,ret1-ret5)
        
inlist=['对数营收','预收账款于营收占比','预收账款同比增速','应收账款周转率','存货周转率','销售费用率','销售毛利率同比',
        'ROE','净利润增长率','营业收入增长率','归母净利润增长率','经营净现金流同比']
       
chart4=pd.DataFrame(index=['','对数营收','对数营收','对数营收','对数营收','对数营收','预收账款于营收占比',
                           '预收账款于营收占比','预收账款于营收占比','预收账款于营收占比','预收账款于营收占比',
                           '预收账款同比增速','预收账款同比增速','预收账款同比增速','预收账款同比增速','预收账款同比增速',
                           '应收账款周转率','应收账款周转率','应收账款周转率','应收账款周转率','应收账款周转率',
                           '存货周转率','存货周转率','存货周转率','存货周转率','存货周转率','销售费用率','销售费用率',
                           '销售费用率','销售费用率','销售费用率','销售毛利率同比','销售毛利率同比','销售毛利率同比',
                           '销售毛利率同比','销售毛利率同比','ROE','ROE','ROE','ROE','ROE','净利润增长率',
                           '净利润增长率','净利润增长率','净利润增长率','净利润增长率','营业收入增长率','营业收入增长率',
                           '营业收入增长率','营业收入增长率','营业收入增长率','归母净利润增长率','归母净利润增长率',
                           '归母净利润增长率','归母净利润增长率','归母净利润增长率','经营净现金流同比','经营净现金流同比',
                           '经营净现金流同比','经营净现金流同比','经营净现金流同比'],
                    columns=['分组','行业','行业','酒类','酒类','食品','食品','饮料','饮料'])

chart4.iloc[0,:]=['','年化超额收益率','胜率','年化超额收益率','胜率','年化超额收益率','胜率','年化超额收益率','胜率']

chart4.iloc[:,0]=['','第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组'
           ,'第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组'
           ,'第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组'
           ,'第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组'
           ,'第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组'
           ,'第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组']
        
for i in range(len(inlist)):
    for j in range(len(glist)):
        if glist[j]=='行业':
           data=pd.read_excel("原始数据.xlsx",sheet_name=inlist[i])
           mid=groups(inlist[i], glist[j])[0]
        else:
           data=pd.read_excel("原始数据.xlsx",sheet_name=inlist[i])
           data=data[data['二级分类']==glist[j]]
           mid=groups(inlist[i], glist[j])[0]
        ret1=np.power((mid.iloc[0,:]+1).prod(),0.1)-1
        ret2=np.power((mid.iloc[1,:]+1).prod(),0.1)-1
        ret3=np.power((mid.iloc[2,:]+1).prod(),0.1)-1
        ret4=np.power((mid.iloc[3,:]+1).prod(),0.1)-1
        ret5=np.power((mid.iloc[4,:]+1).prod(),0.1)-1
        winrate1=((mid.iloc[0,:]-binret)>0).astype(int).sum()/len(binret)
        winrate2=((mid.iloc[1,:]-binret)>0).astype(int).sum()/len(binret)
        winrate3=((mid.iloc[2,:]-binret)>0).astype(int).sum()/len(binret)
        winrate4=((mid.iloc[3,:]-binret)>0).astype(int).sum()/len(binret)
        winrate5=((mid.iloc[4,:]-binret)>0).astype(int).sum()/len(binret)

        chart4.iloc[5*i+1:5*i+6,2*j+1]=(ret1,ret2,ret3,ret4,ret5)
        chart4.iloc[5*i+1:5*i+6,2*j+2]=(winrate1,winrate2,winrate3,winrate4,winrate5)

#对不同的指标，输出不同分类的5组合集收益率
def itn(index):
    agret=pd.DataFrame(columns=['分组','201001','201002','201003','201004','201101','201102','201103','201104',
                                '201201','201202','201203','201204','201301','201302','201303','201304','201401',
                                '201402','201403','201404','201501','201502','201503','201504','201601','201602',
                                '201603','201604','201701','201702','201703','201704','201801','201802','201803',
                                '201804','201901','201902','201903','201904'],index=['行业','行业','行业','行业',
                                '行业','酒类','酒类','酒类','酒类','酒类','食品','食品','食品','食品','食品','饮料',
                                '饮料','饮料','饮料','饮料'])
    agret['分组']=('第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组',
         '第一组','第二组','第三组','第四组','第五组','第一组','第二组','第三组','第四组','第五组')
    
    data=pd.read_excel("原始数据.xlsx",sheet_name=index)
    
    saret=pd.DataFrame()
    
    for i in range(len(glist)):
        if glist[i]=='行业':
           mid=groups(index, glist[i])
        else:
           data=data[data['二级分类']==glist[i]]
           mid=groups(index, glist[i])
        agret.iloc[5*i:5*i+5,1:]=np.array(mid[0])
        saret=pd.concat([saret,mid[1]])
    
    return agret,saret

inlist=['对数营收','预收账款于营收占比','预收账款同比增速','应收账款周转率','存货周转率','销售费用率','销售毛利率同比',
        'ROE','净利润增长率','营业收入增长率','归母净利润增长率','经营净现金流同比']

agr1=itn('对数营收')  
agr2=itn('预收账款于营收占比')
agr3=itn('预收账款同比增速')   
agr4=itn('应收账款周转率')   
agr5=itn('存货周转率') 
agr6=itn('销售费用率')
agr7=itn('销售毛利率同比')
agr8=itn('ROE')
agr9=itn('净利润增长率')
agr10=itn('营业收入增长率')
agr11=itn('归母净利润增长率')
agr12=itn('经营净现金流同比')
    
agret1=agr1[0]    
asret1=agr1[1]
agret2=agr2[0]    
asret2=agr2[1]
agret3=agr3[0]    
asret3=agr3[1]
agret4=agr4[0]    
asret4=agr4[1]
agret5=agr5[0]    
asret5=agr5[1]
agret6=agr6[0]    
asret6=agr6[1]
agret7=agr7[0]    
asret7=agr7[1]
agret8=agr8[0]    
asret8=agr8[1]
agret9=agr9[0]    
asret9=agr9[1]
agret10=agr10[0]    
asret10=agr10[1]
agret11=agr11[0]    
asret11=agr11[1]
agret12=agr12[0]    
asret12=agr12[1]
    
    