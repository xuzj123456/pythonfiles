# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

url = 'https://www.zhihu.com/explore'
browser = webdriver.Chrome()
try:
    browser.get(url)
    # input = browser.find_element_by_id('kw')        # keyword
    # input.send_keys('Python')
    # input.send_keys(Keys.ENTER)
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    # print(browser.current_url)
    # print(browser.get_cookies())
    # print(browser.page_source)      # 网页源代码
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    browser.execute_script('alert("To Bottom")')
    time.sleep(5)
finally:
    browser.close()
