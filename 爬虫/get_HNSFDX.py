# -*- coding: UTF-8 -*-

import urllib2
import urllib
import re

class HNSFDX:
    """http://www.henannu.edu.cn/2017/1017/c8955a104083/page.htm"""
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent' :self.user_agent}

    def getHtml(self):
        try:
            url = 'http://www.henannu.edu.cn/2017/1017/c8955a104083/page.htm'
            requset =urllib2.Request(url ,headers = self.headers)
            response = urllib2.urlopen(requset)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr (e,'reason'):
                print u"Error please try again"
                return None

    def getContent(self):
        pageCode = self.getHtml()
        pattern =re.compile('<a .*?>(.*?)</i>',re.S)
        '''
        <meta name="description" content="..."/>
        '''
        items = re.findall(pattern,pageCode)

        pageStories = []

        for item in items:
            pageStories.append(item[0])
            return pageStories

    def start(self):
        self.getContent()
        pass

spider = HNSFDX()
spider.start()

