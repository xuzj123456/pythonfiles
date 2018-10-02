# coding=utf-8
import requests, re, time, xlwt


def getHtlmText(page_start):        # page_start指该页开始的电影序号-1，用于url
    if page_start != 0:
        kw = {'start': page_start, 'filter': ''}
    else:
        kw = {}

    response = requests.get(url, params=kw, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = "utf-8"
    return response.text


def getData(html):
    movie_li = re.findall(r'<span class="title">(.*?)</span>.*?<span class="rating_num" '
                          r'property="v:average">(...)</span>', html, re.S)

    for each in movie_li:
        print(each[0]+' '+each[1])

    return movie_li     # movie_li为电影列表


if __name__ == '__main__':
    url = 'https://movie.douban.com/top250'
    k = 0       # k用于代入page_start
    i = 1       # i用于填写excel表格
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')
    sheet.write(0, 0, '电影名称')
    sheet.write(0, 1, '豆瓣评分')

    while k <= 225:
        movie_list = getData(getHtlmText(k))
        for each_movie in movie_list:
            sheet.write(i, 0, each_movie[0])
            sheet.write(i, 1, each_movie[1])
            i += 1

        k += 25
        time.sleep(1)

    xl_title = u'豆瓣TOP250.xls'
    wbk.save(xl_title)
