# -*- coding: UTF-8 -*-

import urllib2
import urllib
import re
import os


"""https://www.zhihu.com/question/34378366"""


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
headers = {'User-Agent':user_agent}

def getImg(html):
    imglist = re.findall('img src = "(http.*?)"',html)
    return imglist

request = urllib2.Request('https://www.zhihu.com/question/34378366', headers = headers)
response = urllib2.urlopen(request)
html = response.read().decode('utf-8')

imagesUrl = getImg(html)

if os.path.exists("D:/imags") == False: # 路径存在则返回True,路径损坏返回False
    os.mkdir("D:/imags") # 创建一个在 D 盘为 imags 的文件夹

count = 0
for url in imagesUrl:
    print(url)
    if (url.find('.') != -1):
        name = url[url.find('.',len(url) - 5):];
        request = urllib2.Request(url,headers = headers)
        bytes = urllib2.urlopen(request)
        f = open("D:/imags/"+str(count)+name, 'wb')
        # open(路径+文件名,读写模式)
        # wb 以二进制写模式打开
        f.write(bytes.read())
        f.flush() # 刷新
        f.close() # 关闭
        count+=1
        print 'g'


