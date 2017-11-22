# -*- coding: UTF-8 -*-

import urllib2
import urllib
import re


class TP:
    """https://www.deviantart.com/"""
    """https://www.deviantart.com/?offset=48"""
    def __init__(self):
        self.offset = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent' : self.user_agent}


    def getHtml(self, offset):
        try:
            url = 'https://www.deviantart.com/' + '?' + str(offset)
            request = urllib2.Request(url , headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError,e:
            if hasattr(e , 'reason') :
                print u"Error please try again"
                return None

    def getImg(self):
        x = 0
        def getImg2(self):
            pageCode = self.getHtml(self)
            pattern = re.compile('src="(.*?\.png)"',re.S)
            items = re.findall(pattern,pageCode)
            for item in items:
                urllib.urlretrieve(item, '%s.png' %x)
                x+=1
        return getImg2

    def start(self):
        self.getImg()
        pass

spider = TP()
spider.start()



