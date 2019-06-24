# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.w3cschool.cn/nodejs/nodejs-tutorial'
# collections/后面的16代表程序员专题.
# order_by=added_at代表按收录时间排序
# page = 1 页数

add_url = 1
# 获取页数

num = 0
# 文章计数标题


try:
        page = requests.request('get', base_url%add_url).content
        # 将基础网址和页数拼接得到'实际网址'
        # 使用request的get方法获取响应
        # 再用content方法'得到内容'

        soup = BeautifulSoup(page, 'lxml')
        # 分析页面

        article_list = [i.get_text() for i in soup.select(".title a")]

        for i in article_list:
            num+=1
            print(num,'',i)
            pass
        add_url +=1
        pass
except Exception as e:
        print(e)








