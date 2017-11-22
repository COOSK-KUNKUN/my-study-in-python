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
    os.mkdir("D:/image")
    pass

count = 0

for url in imagesUrl:
    print(url)
    if (url.find('.') != -1):
        name = url[url.find('.',len(url) - 5):];
        request = urllib2.Request(url,headers = headers)
        bytes = urllib2.urlopen(request)
        f = open("D:/image/" + str(count) + name, "wb")
        f.write(bytes.read())
        f.flush()
        f.close()
        count+=1
        print 'get it'
        pass
    pass