# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import thread

class Tool:
    """docstring for Tool"""
    removeImg = re.compile('<img.*?>| {7}|')
    # 去除img标签

    removeAddr = re.compile('<a.*?>|</a>')
    # 去除 <a herf = >标签

    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 替换 tr 标签为\n

    replaceTD = re.compile('<td>')
    # 替换 td 标签为\t

    replacePara = re.compile('<p.*?>')
    # 把段落开头换为\n加空两格

    replaceBR = re.compile('<br><br>|<br>')
    # 将换行符或双换行符替换为\n

    def replace(self, x):
        x= re.sub(self.removeImg, '', x)
        x= re.sub(self.removeAddr, '', x)
        x= re.sub(self.replaceLine,'\n',x)
        x= re.sub(self.replaceTD,'\t',x)
        x= re.sub(self.replacePara,'\n  ',x)
        x= re.sub(self.replaceBR, '\n',x)
        return x.strip()
        # strip()替换


class BDTB:
    """docstring for BDTB"""
    def __init__(self, baseUrl, seeLZ):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.heads = {'User-Agent':self.user_agent}

        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        # see_lz和pn是该URL的两个参数，分别代表了只看楼主和帖子页码

        self.tool = Tool()

    # 初始化，传入基地址，是否只看楼主的参数

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            requset = urllib2.Request(url)
            response = urllib2.urlopen(requset)
            return response.read().decode('utf-8')
            # 将页面转化为UTF-8编码

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"Error please try again",e.reason
                return None
    # 传入页码，获取该页帖子的代码

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h1 class="core_title_txt.*?">(.*?)</h1>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    # 获取帖子标题

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?span*？>(.*?)</div>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None
    # 获取帖子一共有多少页

    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern, page)
        print self.tool.replace(items[1])
    # 获取每一层楼的内容,传入页面内容



baseURL = "http://tieba.baidu.com/p/3138733512"
bdtb = BDTB(baseURL, 1) # 等于1表示该条件为真
bdtb.getContent(bdtb.getPage(1))

