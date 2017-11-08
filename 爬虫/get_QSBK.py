# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import thread
import time

class QSBK:
    """初始化方法"""
    def __init__(self):
        self.pageIndex = 1
        # 开始的页数

        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':self.user_agent}

        self.stories = []
        #存放段子的变量，每一个元素是每一页的段子们

        self.enable = False
        # 存放程序是否继续运行的变量

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)

            pageCode = response.read().decode('utf-8')
            # 将页面转化为UTF-8编码

            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Error,please try again",e.reason
                return None
    # 传入某一页的索引获得页面代码

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "Error,please try again!"
            return None

        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        # (.*?)代表一个分组
        # item[0]就代表第一个(.*?)所指代的内容
        # item[1]就代表第二个(.*?)所指代的内容，以此类推。

        items = re.findall(pattern,pageCode)
        # 存储每页的段子

        pageStories = []
        # 遍历正则表达式匹配的信息

        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])

        """
            haveImg = re.search('img',item[3])

            if not haveImg:
                replaceBR = re.compile('<br/>')
                # 返回 br 对象

                text = re.sub(replaceBR, '\n',item[1])
                # re.sub(pattern, repl, string[, count])
                # 替换

                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
                # item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
                # str.strip([chars]) 用于移除字符串头尾指定的字符
                # chars -- 移除字符串头尾指定的字符。
        """
        return pageStories
    # 传入某一页代码，返回本页不带图片的段子列表

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2: # 如果当前未看的页数少于2页，则加载新一页

                pageStories = self.getPageItems(self.pageIndex)
                # 获取新一页

                if pageStories: # 将该页的段子存放到全局list中
                    self.stories.append(pageStories)
                    self.pageIndex +=1
                    # 获取完之后页码索引加一，表示下次读取下一页

    # 加载并提取页面的内容，加入到列表中

    def getOnStory(self,pageStories,page):
        for story in pageStories:# 每遍历一个段子就..
            input = raw_input()
            # 等待用户输入
            # 回车

            self.loadPage()
            # 每当输入回车一次，判断一下是否要加载新页面

            if input == "N":
                self.enable = False
                return
            print u"第%d页\t 发布人: %s\t 赞:%s\n%s" % (page,story[0],story[2],story[1])
            '''
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" % (page,story[0],story[2],story[3],story[1])
            '''
    def start(self):
        print u"Loading,please put 'Enter' to watch or put 'N' to exit"
        self.enable = True
        #使变量为True，程序可以正常运行

        self.loadPage() # 先加载一页内容
        nowPage = 0
        while self.enable: # #局部变量，控制当前读到了第几页
            if len(self.stories)>0:
                pageStories = self.stories[0]
                # #从全局list中获取一页的段子

                nowPage += 1
                # 当前读到的页数加一

                del self.stories[0]
                # 将全局list中第一个元素删除，因为已经取出
                # del 删除变量

                self.getOnStory(pageStories,nowPage)
                # 输出该页的段子

spider = QSBK()
spider.start()