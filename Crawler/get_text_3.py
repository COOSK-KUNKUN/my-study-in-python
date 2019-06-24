# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User_agent':user_agent}

url = 'http://www.rarbt.com/'
request = urllib2.Request(url, headers = headers)
response = urllib2.urlopen(request)
html = response.read().decode('utf-8')

def getImg(html):
    imglist = re.findall('img src="(http.*?)"',html)
    return imglist
    pass

imagesUrl = getImg(html)

if os.path.exists("D:/image") == False :
# 路径存在则返回True,路径损坏返回False

    os.mkdir("D:/image")
    # 创建一个在 D 盘为 imags 的文件夹
    pass

count = 0

for url in imagesUrl:
    print(url)
    if (url.find('.') != -1):
        name = url[url.find('.',len(url) - 5):];
        request = urllib2.Request(url,headers = headers)
        bytes = urllib2.urlopen(request)
        f = open("D:/image/" + str(count) + name, "wb")
        # open(路径+文件名,读写模式)
        #读写模式:r只读,r+读写,w新建(会覆盖原有文件),a追加,b二进制文件.常用模式

        f.write(bytes.read())
        f.flush() # 刷新
        f.close() # 关闭文件
        count+=1
        print 'get it'
        pass
    pass