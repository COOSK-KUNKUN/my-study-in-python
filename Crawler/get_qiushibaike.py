# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re

page = 1

addUrl = 'http://www.qiushibaike.com/hot/page/' + str(page)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

try:
    request = urllib2.Request(addUrl,headers = headers)
    response = urllib2.urlopen(request)

    content = response.read().decode('utf-8')
    pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    # .*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符
    # ？表示使用非贪婪模式进行匹配
    # (.*?)代表一个分组
    # item[0]就代表第一个(.*?)所指代的内容
    # item[1]就代表第二个(.*?)所指代的内容，以此类推。
    # re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。

    items = re.findall(pattern,content)

    for item in items:
        haveImg = re.search("img",item[3])
        # 判断item[3]中是否含有img标签

        if not haveImg:
            print item[0],item[1],item[2],item[4]


except urllib2.URLError , e:
    if hasattr(e,'code'):
        print e.code
    if hasattr(e,'reason'):
        print e.reason
