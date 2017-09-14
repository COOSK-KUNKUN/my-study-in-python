# -*- coding: UTF-8 -*-
import urllib
import re

HEADER = {
    "Host": "tieba.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}

def getHtml( url ):
	page = urllib.urlopen(url)
	html = page.read()
	return html

# Urllib 模块提供了读取web页面数据的接口,可以像读取本地文件一样读取www和ftp上的数据
# urllib.urlopen()方法用于打开一个URL地址
# read()方法用于读取URL上的数据，向getHtml()函数传递一个网址，并把整个页面下载下来

def getImg( html ):
	reg = r'src = "([^ >]+?\.jpg)" pic_ext'    # .*?\.jpg\?.*?
	imgre = re.compile( reg )
	imglist = re.findall( imgre, html )
	x = 0
	for imgurl in imglist:
   		urllib.urlretrieve(imgurl,'%s.jpg' % x)
        x+=1
   	return imglist


html = getHtml('http://tieba.baidu.com/p/4574798123')

print getImg(html)


