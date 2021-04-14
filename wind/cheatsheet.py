# coding=utf-8

#  所有a股
#  all_a = w.wset("SectorConstituent",date = date ,sector=u"全部A股")
#  all_Code = list(pd.Series(all_a.Data[1]))

#   停牌股
#  all_tp = w.wset("TradeSuspend",startdate = date,enddate = date,field = "wind_code,sec_name,suspend_type,suspend_reason")
#  all_tp_code = list(pd.Series(all_tp.Data[0]))

#  所有st
#  all_st = w.wset("SectorConstituent",date=date,sector=u"风险警示股票",field="wind_code,sec_name")
#
#  all_st_code = list(pd.Series(all_st.Data[0]))

#  all_Code = set(all_Code)
#  all_st_code = set(all_st_code)
#  all_tp_code = set(all_tp_code)
#   code = all_Code - all_tp_code - all_st_code

##########################################################################