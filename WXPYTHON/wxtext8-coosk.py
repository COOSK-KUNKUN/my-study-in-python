# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,400))

        size.InitUI(self)

    def InitUI(self):
        self.count = 0
        panel = wx.Panel(self)
        box = wx.SizeBOX(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL) 
        box2 = wx.BoxSizer(wx.HORIZONTAL)

        self.Gauge = wx.Gauge(panel, range = 20 , size = (250,25), style = wx.GA_HORIZONTAL)
        # wx.Gauge(parent, id, range, pos, size, style)
        # Wx.Gauge类对象表示垂直或水平条，其中以图形方式显示递增量。
        
        self.button = wx.Button(panel, label = "Start")
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button)

        box1.Add(self.gague, proportion = 1, style = wx.ALIGN_CENTRE)



        pass