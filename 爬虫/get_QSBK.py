# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import thread
import time

class QSBK(object):
    """docstring for QSBK"""
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':self.user_agent}

        self.stories = []
        #存放程序是否继续运行的变量

        self.enable = False
    # 传入某一页的索引获得页面代码

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)

            pageCode = response.read().decode('utf-8')
            # 将页面转化为UTF-8编码

            return pageCode

            pass
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Error",e.reason
                return None
                pass
        pass
    # 传入某一页代码，返回本页不带图片的段子列表

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "Error"
            return None
            pass

        pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)

        items = re.findall(pattern,pageCode)
        pass