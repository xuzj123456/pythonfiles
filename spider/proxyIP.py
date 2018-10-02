# coding=utf-8
import requests
import random
import time
import re

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 '
    '(KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
    '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]


def get_proxy_ip_list():
    headers = {
        'Referer': 'http://www.xicidaili.com/',
        'User-Agent': random.choice(user_agent_list)
    }
    response = requests.get('http://www.xicidaili.com/nn/', headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    ip_list = re.findall(r'(\d+\.+\d+\.+\d+\.+\d).*?<td>(\d+)</td>', html, re.S)  # 需要ip地址和端口
    proxy_ip_list = []
    for k in ip_list:
        proxy = '{}:{}'.format(k[0], k[1])  # ip地址格式
        proxy_ip_list.append(proxy)

    return proxy_ip_list


def proxy_ip_read(proxy_ip_list, user_agent_list, i):
    proxy_ip = {'http': 'http://' + proxy_ip_list[i]}
    user_agent = random.choice(user_agent_list)
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time)
    headers = {
        'User-Agent': user_agent
    }
    try:
        html = requests.get('http://httpbin.org/ip', headers=headers, proxies=proxy_ip).text  # 该网址用来测试ip地址
    except Exception:
        print('***ip{}代理失败***'.format(proxy_ip_list[i]))
        break_flag = False
        return [break_flag]
    else:
        print('***ip{}代理成功***'.format(proxy_ip_list[i]))
        break_flag = True
        return [break_flag, proxy_ip]


def main():
    proxy_ip_list = get_proxy_ip_list()
    for i in range(len(proxy_ip_list) - 1):
        result = proxy_ip_read(proxy_ip_list, user_agent_list, i)
        if result[0]:
            print(result[1])
            return result[1]


def get_user_agent():
    return random.choice(user_agent_list)


if __name__ == '__main__':
    main()
