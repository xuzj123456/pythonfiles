# -*- coding:utf-8 -*-
import data_cycle_lib.best_corr_CI_DI as  CCD
import matplotlib.pyplot as plt
import pandas as pd
import re, os
import data_cycle_lib.cycle_lib as cycle_tool
import data_cycle_lib.data_clean_lib as  clean_tool
import data_cycle_lib.cycle_X13 as  cycle_X13


def year_add2month(pf):
    list_new = []
    for i in range(len(pf)):
        item = ""
        month_str = int(pf.index[i].split("-")[1])

        # 不是从1月份开始的
        if i == 0 and month_str != 1:
            item = pf[i] / month_str
        else:
            if month_str == 1:
                item = pf[i]
            else:
                item = pf[i] - pf[i - 1]
        list_new.append(item)
    print(list_new)
    return pd.Series(list_new, pf.index)


# 累计值转当月值
def all2month(pf):
    cols = pf.columns.tolist()
    print(pf)
    for item in cols:
        if re.search("累计值$", item) and item.replace("累计值", "当月值") not in cols:
            pf[item.replace("累计值", "当月值(累_计值转换)")] = year_add2month(pf[item])
            pf[item.replace("累计值", "当月值(累_计值转换)_同比")] = get_tongbi(year_add2month(pf[item]))
    print(pf)
    # print(pf[item])
    # print(pf[item.replace("累计值","当月值")])
    # raise
    return pf


# 同步
def get_tongbi(df, step=12):
    """
    月份数据 生成同步序列
    """
    # 同比步长，12个月
    df_2 = df.shift(step)
    df_sy = 100 * (df - df_2) / df_2

    return df_sy.dropna()


# hp_滤波，返回周期项
def hp_lb_c(df):
    clean_tool_ = clean_tool.Pd_Info()
    step = 14400  # 月度数据14400
    df = df.dropna()
    return clean_tool_.hp_lb(df, step, True)[1]


# 获取各种相关系数
def main():
    ccd = CCD.CI_AND_DI()  # 获取数据

    ccd.main_CI_DI(3, 10, data_check_name="dataand申万行业指数_白酒_月_20-01_原始数据处理后_original_2020-02-12 16-04-01.csv",
    best_pd_name="dataand申万行业指数_白酒_月_2007-01_最优相关系数_original_2020-02-12 16-04-01.csv")

    # ccd.main_CI_DI(3,10,data_check_name="汽车行业数据汇总（月度数据）_月频数据_new_all 原始数据处理后_hp_hp __2019-11-14 15-10-30.csv",
    # # best_pd_name="汽车行业数据汇总（月度数据）_月频数据_new_all  最优相关系数_hp_hp __2019-11-14 15-10-30.csv")

    # 国债  中债10年期国债指数_同比
    # ccd.get_best_corr_data("国债数据  中债10年期国债指数_同比.xlsx",index_file_name="月频数据_new_all_2019-11-20.xlsx",move_len=12,data_process ="hp")  #获取周期数据及最优相关系数
    # ccd.main_CI_DI(3,10,data_check_name="国债数据  中债10年期国债指数_同比_月频数据_new_all_2019-11-20 原始数据处理后_hp_hp __2019-11-20 15-48-52.csv",
    # best_pd_name="国债数据  中债10年期国债指数_同比_月频数据_new_all_2019-11-20  最优相关系数_hp_hp __2019-11-20 15-48-52.csv")

    # ccd.get_best_corr_data("国债数据 中债国债到期收益率10年_3阶差分.xlsx",
    # index_file_name="月频数据_new_all_2019-11-20.xlsx",move_len=12,data_process ="hp")  #获取周期数据及最优相关系数

    # 国债  中债10年期国债指数_12阶差分
    # ccd.get_best_corr_data("中债国债到期收益率10年_12阶差分.xlsx",
    # index_file_name="宏观月频_填充07(1).xlsx",move_len=12,data_process ="")  #获取周期数据及最优相关系数

    # 汽车行业：
    # ccd.get_best_corr_data("X13_月频数据_new_11-20_2019-11-21 08-53-06.xlsx"
    # ,move_len=12,data_process ="hp")  #获取周期数据及最优相关系数

    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_月频数据_new_11-20_2019-11-21 08-53-06_  最优相关系数_hp_hp __2019-11-21 10-49-17.csv",
    # data_check_name="X13_月频数据_new_11-20_2019-11-21 08-53-06_ 原始数据处理后_hp_hp __2019-11-21 10-49-17.csv")

    # # ccd.main_CI_DI(3,10,
    # best_pd_name="汽车宏观综合指标(1)_  最优相关系数_hp_cycle_hp_cycle __2019-11-20 17-19-49.csv",
    # data_check_name="汽车宏观综合指标(1)_ 原始数据处理后_hp_cycle_hp_cycle __2019-11-20 17-19-49.csv")

    # #万得全A
    # ccd.get_best_corr_data("X13_宏观月频_填充_11-25_2019-11-25 10-59-36_and_万得全A_同比.xlsx",move_len=12,data_process ="hp")  #获取周期数据及最优相关系数

    # 国债
    # ccd.get_best_corr_data("X13_月频数据_new_10年国债指数同比.xlsx",move_len=12,data_process ="hp")  #获取周期数据及最优相关系数
    # ccd.get_best_corr_data("X13_月频数据_new_中债10年期国债指数.xlsx",move_len=12,data_process ="hp")  #获取周期数据及最优相关系数

    # 10年国债指数同比
    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_月频数据_new_10年国债指数同比_  最优相关系数_hp_hp __2019-11-22 08-57-38.csv",
    # data_check_name="X13_月频数据_new_10年国债指数同比_ 原始数据处理后_hp_hp __2019-11-22 08-57-38.csv")

    # #国债到期收益率10年_12阶差分
    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_月频数据_new_国债到期收益率10年_12阶差分_  最优相关系数_hp_hp __2019-11-22 13-18-17.csv",
    # data_check_name="X13_月频数据_new_国债到期收益率10年_12阶差分_ 原始数据处理后_hp_hp __2019-11-22 13-18-17.csv")

    # 中债国债到期收益率:10年
    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_月频数据_new_中债国债到期收益率10年_  最优相关系数_hp_hp __2019-11-22 14-25-05.csv",
    # data_check_name="X13_月频数据_new_中债国债到期收益率10年_ 原始数据处理后_hp_hp __2019-11-22 14-25-05.csv")

    # #中债10年期国债指数
    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_月频数据_new_中债10年期国债指数_  最优相关系数_hp_hp __2019-11-22 14-53-51.csv",
    # data_check_name="X13_月频数据_new_中债10年期国债指数_ 原始数据处理后_hp_hp __2019-11-22 14-53-51.csv")

    # ccd.main_CI_DI(3,10,
    # best_pd_name="X13_宏观月频_填充_2019-11-24 13-54-59_2008-02_2015-06_  最优相关系数_original_original __2019-11-24 15-18-48.csv",
    # data_check_name="X13_宏观月频_填充_2019-11-24 13-54-59_2008-02_2015-06_ 原始数据处理后_original_original __2019-11-24 15-18-48.csv",
    # original_name = "CBA02701.CS_month.xlsx")


# 归一化处理
# x' = (x - X_min) / (X_max - X_min)
def get_guiyi(df):
    max = df.max()
    min = df.min()
    return (df - min) / (max - min)


# X13循环跑--add 同比 --相关性 -- 最优合成CI--预测同比--同比恢复到指数
def X13_cycle_main():
    ccd = CCD.CI_AND_DI("dict_type11-25.csv", )  # 获取数据
    # 循环：
    name = "宏观月频_填充.xlsx"  # 宏观数据
    ccd.get_best_corr_data(name, move_len=12, data_process="original")
    raise
    clean_tool_ = clean_tool.Pd_Info()
    pf_all = clean_tool_.data_day2month(name).dropna()
    print(pf_all)
    pf_all = pf_all.truncate(before="%s-%s" % ("2008", "2".zfill(2)))
    for i in range(12, len(pf_all), 12):
        if i + 89 <= len(pf_all):
            # pf_cut = pf_all[i:i+89]
            # print(pf_cut)
            # cut_name = "%s_%s_%s.xlsx"%(name.split(".")[0],pf_cut.index[0],pf_cut.index[-1])
            # pf_cut.to_excel(cut_name)

            # X13_file_name = cycle_X13.get_x13(cut_name,pf_cut.index[0].split("-")[0],pf_cut.index[0].split("-")[1])
            # #X13_file_name = "X13_宏观月频_填充_2008-02_2015-06_2019-11-24 15-59-52.csv"
            # #合并同比和宏观数据
            base_name = "CBA02701.CS_month.xlsx"
            # pf_base = clean_tool_.data_day2month(base_name).dropna()
            # pf_base = pf_base[pf_base.columns.tolist()[0]]
            # pf_cut_x13 = clean_tool_.data_day2month(X13_file_name)
            # pf_tb = get_tongbi(pf_base) #获取同比序列
            # pf_tb.name = "%s_同比（12月）"%base_name.split(".")[0]

            # pf_cut_x13_and_tb = pd.concat([pf_tb,pf_cut_x13],axis = 1,sort =False).dropna()
            # print(pf_cut_x13_and_tb)
            # pf_cut_x13_and_tb["date"] = pf_cut_x13_and_tb.index
            # cut_name_x13_and_tb = "%s_and_%s.xlsx"%(X13_file_name.split(".")[0],base_name.split(".")[0])
            # pf_cut_x13_and_tb.to_excel(cut_name_x13_and_tb,index=False)

            # #CBA02701
            # #获取最优相关
            # data_check_name,best_pd_name = ccd.get_best_corr_data(cut_name_x13_and_tb,move_len=12,data_process ="original")  #获取周期数据及最优相关系数

            # #2017
            # # data_check_name = "X13_宏观月频_填充_2010-02_2017-06_2019-11-25 08-57-57_and_CBA02701_ 原始数据处理后_original_original __2019-11-25 09-16-59.csv"
            # # best_pd_name = "X13_宏观月频_填充_2010-02_2017-06_2019-11-25 08-57-57_and_CBA02701_  最优相关系数_original_original __2019-11-25 09-16-59.csv"
            # # #2019
            # # data_check_name = "X13_宏观月频_填充_2012-02_2019-06_2019-11-25 09-39-31_and_CBA02701_ 原始数据处理后_original_original __2019-11-25 10-00-03.csv"
            # # best_pd_name = "X13_宏观月频_填充_2012-02_2019-06_2019-11-25 09-39-31_and_CBA02701_  最优相关系数_original_original __2019-11-25 10-00-03.csv"
            # #2018
            # # data_check_name = "X13_宏观月频_填充_2011-02_2018-06_2019-11-25 09-17-36_and_CBA02701_ 原始数据处理后_original_original __2019-11-25 09-38-27.csv"
            # # best_pd_name = "X13_宏观月频_填充_2011-02_2018-06_2019-11-25 09-17-36_and_CBA02701_  最优相关系数_original_original __2019-11-25 09-38-27.csv"
            # # #2016
            # # data_check_name = "X13_宏观月频_填充_2009-02_2016-06_2019-11-24 17-00-31_and_CBA02701_ 原始数据处理后_original_original __2019-11-24 17-20-25.csv"
            # # best_pd_name = "X13_宏观月频_填充_2009-02_2016-06_2019-11-24 17-00-31_and_CBA02701_  最优相关系数_original_original __2019-11-24 17-20-25.csv"
            # # #2015
            # data_check_name = "X13_宏观月频_填充_2008-02_2015-06_2019-11-24 15-59-52_and_CBA02701_ 原始数据处理后_original_original __2019-11-24 16-57-13.csv"
            # best_pd_name = "X13_宏观月频_填充_2008-02_2015-06_2019-11-24 15-59-52_and_CBA02701_  最优相关系数_original_original __2019-11-24 16-57-13.csv"

            # 根据最优相关，合成CI
            ccd.main_CI_DI(3, 10,
                           best_pd_name=best_pd_name,
                           data_check_name=data_check_name,
                           original_name=base_name)
            raise


# 画图，累计值转换
def do_some():
    name = "CBA02701.CS_month.xlsx"
    pf = pd.read_excel(name)
    pf = pf.set_index("date")
    print(pf)
    pf_hp = hp_lb_c(pf[pf.columns.tolist()[0]])
    plt.show()
    raise
    sz_cycle = cycle_tool.Cycle_PF(pf_hp, 1)
    sz_cycle.get_fft_top()
    sz_fft = sz_cycle.show_fft()
    freqs_list = sz_cycle.get_fft_top()[0]

    base_fit_42_gau = sz_cycle.cycle_fit_by_gau(45)

    # plt.show()

    # # pf =all2month(pf[pf.columns.tolist()[1:3]])
    # # pf.to_csv("%s_当月.csv"%name.split(".")[0])


# 均方误差（mean-square error, MSE）
def Accuracy_test():
    filedir_path = os.path.join(os.getcwd(), "predict_1")
    file_list = os.listdir(filedir_path)
    clean_tool_ = clean_tool.Pd_Info()
    for file_name in file_list:
        if not re.search("csv$", file_name):
            continue
        file_path = os.path.join(filedir_path, file_name)
        print("file_path", file_path)
        split_file_name = file_name.split("_")
        predict_date = split_file_name[5]
        print("predict_date", predict_date)
        # print(predict_date)
        # raise
        pf_old = clean_tool_.data_day2month(file_path)
        pf_all = pf_old.truncate(before="%s-%s" % (predict_date.split("-")[0],
                                                   str(int(predict_date.split("-")[1]) + 1).zfill(2)))

        cols = pf_all.columns.tolist()
        pf_MSE = (pf_all[cols[2]] - pf_all[cols[1]]) ** 2

        list_mse = []
        for i in range(len(pf_MSE)):
            list_mse.append(pf_MSE[i].sum() / (i + 1))

        pf_mse = pd.Series(list_mse, pf_all.index)
        list_name = split_file_name[:3] + split_file_name[7:10] + split_file_name[4:6] + split_file_name[-1:]
        print(list_name)

        pd_all_mse = pd.concat([pf_old, pf_mse], axis=1, sort=False)
        pd_all_mse.columns = pf_old.columns.tolist() + ["MSE"]

        pd_all_mse[cols[0][:-3]] = get_tongbi(pd_all_mse[cols[1]])

        file_name_mse = "%s_%s_%s_%s_%s_%s_(%s_%s)_MSE_%s" % tuple(list_name)
        pd_all_mse.to_csv(file_name_mse)

        # 画图，保存
        cols = pd_all_mse.columns.tolist()
        ax = pd_all_mse.plot(use_index=True, y=cols[:3] + cols[-1:], figsize=(10, 6),
                             secondary_y=cols[1:3], title="CI指标对比(%s)" % file_name_mse.split(".")[0])
        plt.savefig('%s.png' % file_name_mse.split(".")[0], dpi=200)

        # raise


# hp画图
def hp_plot_test():
    filedir_path = os.path.join(os.getcwd(), "predict_2")
    file_list = os.listdir(filedir_path)
    clean_tool_ = clean_tool.Pd_Info()
    pf_or = clean_tool_.data_day2month("国债数据_月平均 (1).xlsx")
    for file_name in file_list:
        if not re.search("csv$", file_name):
            continue
        file_path = os.path.join(filedir_path, file_name)
        print("file_path", file_path)
        split_file_name = file_name.split("_")

        pf_old = clean_tool_.data_day2month(file_path)
        pf_all = pd.concat([pf_old, pf_or], axis=1, sort=True)
        pf_all.columns = ["超前指标", "hp滤波", "原始值"]
        list_name = split_file_name[:3] + split_file_name[7:10] + split_file_name[4:6] + split_file_name[-1:]
        print(list_name)

        file_name_mse = "%s_%s_%s_%s_%s_%s_(%s_%s)_MSE_%s" % tuple(list_name)
        pf_all.to_csv(file_name_mse)

        pf_all = pf_all.apply(get_guiyi)  # 归一化处理

        # 画图，保存
        cols = pf_all.columns.tolist()
        pf_all[cols[0]] = pf_all[cols[0]].shift(6)
        ax = pf_all.plot(use_index=True, y=cols, figsize=(10, 6),
                         secondary_y=cols[1:], title="CI指标对比(%s)" % file_name_mse.split(".")[0])
        plt.savefig('%s.png' % file_name_mse.split(".")[0], dpi=200)

        # raise


if __name__ == "__main__":
    main()
    # do_some()
    # X13_cycle_main()
    # hp_plot_test()
