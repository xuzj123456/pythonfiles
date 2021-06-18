# coding=utf-8
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import Select

#下载符合版本的chromedriver
chromedriver = r'chromedriver.exe'

options = webdriver.ChromeOptions()
#不呼出浏览器
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")

driver = webdriver.Chrome(chromedriver, chrome_options=options)

url = 'https://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html'
driver.get(url)

s1 = Select(driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div[2]/div[2]/label/select'))
s1.select_by_value("100")

element = driver.find_element_by_id('dvccFundList_info')
text = element.text
n_total = int(text.split('条')[0][1:])
n = int(n_total/100)

df = pd.DataFrame(columns=['产品编码','产品名称','管理人名称','成立日期'])

for j in range(1, n+1):
    element_ = element
    while element == element_:
        element = driver.find_element_by_id('dvccFundList')
        text = element.text
        text_list = text.split('\n')
        time.sleep(0.5)

    element = driver.find_element_by_class_name('paginate_numbers')
    text = element.text

    m = n_total%100 if j == n else 100
    for i in range(1,m+1):
        i_ = len(df.index)
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/table/tbody/tr[{0}]/td[2]'.format(i))
        df.loc[i_,df.columns[0]] = e.text
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/table/tbody/tr[{0}]/td[3]/a'.format(i))
        df.loc[i_,df.columns[1]] = e.text
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/table/tbody/tr[{0}]/td[4]'.format(i))
        df.loc[i_,df.columns[2]] = e.text
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/table/tbody/tr[{0}]/td[5]'.format(i))
        df.loc[i_,df.columns[3]] = e.text

    if j == 1 or j == 2:
        x = j+1
    elif j == n-1:
        x = 5
    elif j == n:
        break
    else:
        x = 4
    e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div[2]/div[3]/span/a[{0}]'.format(x))
    try:
        ActionChains(driver).move_to_element(e).click(e).perform()
    except Exception as e_:
        print(e_)
        time.sleep(3)
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div[2]/div[3]/span/a[{0}]'.format(x))
        ActionChains(driver).move_to_element(e).click(e).perform()

    time.sleep(2)

for i in df.index:
    if type(df['管理人名称'][i]) == list:
        df['管理人名称'][i] = df['管理人名称'][i][0]

df_=df.drop_duplicates('产品编码')
# for i in range(n_total):
#     if i not in df_.index:
#         print(i)

df_.to_excel('证券资管产品.xlsx', encoding='gbk')

#补充没有获取的时间
for i in df_.index:
    if df_.loc[i, '成立日期'] == '':
        code = df_.loc[i, '产品编码']
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/form/div/table/tbody/tr/td/table/tbody/tr[1]/td[3]/div/input')
        e.clear()
        e.send_keys(code)
        e = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/form/div/table/tbody/tr/td/table/tbody/tr[2]/td[3]/div/div[1]/a/span')
        ActionChains(driver).move_to_element(e).click(e).perform()
        time.sleep(3)
        e = driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[3]/div/div/table/tbody/tr/td[5]')
        df_.loc[i, '成立日期']=e.text

