# -*- coding: UTF-8 -*-

import wx

class text(wx.Frame):
    """docstring for text"""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (300,200))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        # wx.TE_MULTILINE:文本控制显示多行

        self.CreateStatusBar()
        # 创建窗口底部状态栏
        
        filemenu = wx.Menu()
        #设置菜单

        filemenu.Append(wx.ID_ABOUT, u"About", u"about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, u"exit", u"终止应用程序")
        #wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, u"flie")
        self.SetMenuBar(menuBar)
        self.Show(True)
        #创建菜单栏

        


app = wx.App(False)

frame = text(None, 'COOSK')

app.MainLoop()

