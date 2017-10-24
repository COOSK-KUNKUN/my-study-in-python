# -*- coding: UTF-8 -*-

import wx
import time

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,400))

        self.InitUI()

    def InitUI(self):
        self.count = 0
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL) 
        box2 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(panel, range = 10 , size = (250,25), style = wx.GA_HORIZONTAL)
        # wx.Gauge(parent, id, range, pos, size, style)
        # Wx.Gauge类对象表示垂直或水平条，其中以图形方式显示递增量。
        # range 读条范围
        
        self.button = wx.Button(panel, label = "Start")
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button)

        box1.Add(self.gauge, proportion = 1, flag = wx.ALIGN_CENTRE)
        box2.Add(self.button, proportion = 1, flag = wx.RIGHT, border = 10)
        # proportion 控制控件相对大小，proportion如果为0，表示默认大小。
        # 比如一个box里面有两个相同控件A，B，如果A，B的proportioin分别为2和1，那么A和B显示出来的大小比例就是2:1.
        # 如果一个box里面有三个相同控件A，B，C，它们的proportion分别为0，1，1，那么A会是默认大小
        # （比如一个只有一行的文本框），B，C平分这个box的其余部分。

        box.Add((0,30))
        box.Add(box1, flag = wx.ALIGN_CENTRE)
        # flag参数与border参数结合指定边距宽度，包括以下选项：
        # wx.LEFT ，左边距
        # wx.RIGHT，右边距
        # wx.BOTTOM，底边距
        # wx.TOP，上边距
        # wx.ALL，上下左右四个边距

        box.Add((0,10))
        box.Add(box2, proportion =  1 ,flag = wx.ALIGN_CENTRE)

        panel.SetSizer(box)
        self.SetSize((300,200))
        self.Centre() 
        self.Show(True)

        pass

    def OnStart(self,event):
        while True:
           
            self.count = self.count + 1
            self.gauge.SetValue(self.count)

            if self.count >= 10:
                print "end"
                return;
                
    def button(self,event):
            self.button.SetValue(2333)
                  
        


app = wx.App()

mycoosk(None, "COOSK")

app.MainLoop()