# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import datetime

base_url = 'http://www.henannu.edu.cn/'

def mycoosk():
    add_url = ''
    # 先置为空字符串

    title_list = []
    # 文章标题列表

    for i in range(15):
        # 首页热门实际为15页，一开始可以设大些让程序自动退出来看到底有多少页

        try:
            page = requests.get(base_url+ add_url).content
            soup = BeautifulSoup(page, "lxml")
            title_list = [i.get_text() for i in soup.select(".title a")]

            try:
                add_url = soup.select(".ladda-button")[-1].get("data-url")
            except :
                break

        except requests.exceptions.ConnectionError:
            # 如果请求过多导致服务器拒绝连接
            status_code = 'Connection refused'
            print(status_code)
            time.sleep(10)
            # 休息10s再爬

        with open('csv','wb') as f:
            spamwriter = csv.writer(f)
            spamwriter.writerow(title_list)


    print ('done')

import time

while True:
    mycoosk()
    time.sleep(10)
