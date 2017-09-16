# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title , size = (350,300))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL) 
        # 整体框架

        #***********************************************#
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        # wx.HORIZONTAL或wx.VERTICAL，表示在水平或垂直方向居中。
        label = wx.StaticText(panel, -1, "单行文本")
        # 文本输入框架注释

        box1.Add(label, 1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        # wx.EXPAND：填满它所处的格子空间。
        # wx.ALL:一个有效的位置或尺寸。
        self.t1 = wx.TextCtrl(panel)

        box1.Add(self.t1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1.Bind(wx.EVT_TEXT,self.OnKeyTyped)
        # wx.EVT_TEXT 响应变化的文本框的内容，或者通过手动键入，或以编程方式
        # Bind 响应文本事件
        # frame.Bind(wx.EVT_TEXT, frame.OnText, text)
        box.Add(box1)

        #***********************************************#
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, -1, "PassWord")

        box2.Add(label1, 1, wx.ALIGN_LEFT|wx.ALL,5)
        self.t2 = wx.TextCtrl(panel, style = wx.TE_PASSWORD)
        # wx.TE_PASSWORD 文本将回显为星号

        self.t2.SetMaxLength(5) 
        # 设置密码的长度

        box2.Add(self.t2, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        box.Add(box2)
        self.t2.Bind(wx.EVT_TEXT_MAXLEN,self.PassWord)
        # wx.EVT_TEXT_MAXLEN
        
        #***********************************************#
        box3 = wx.BoxSizer(wx.HORIZONTAL) 
        label2 = wx.StaticText(panel, -1, "多行文本") 
        
        box3.Add(label2,1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t3 = wx.TextCtrl(panel,size = (200,100),style = wx.TE_MULTILINE) 
        
        box3.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        box.Add(box3) 
        self.t3.Bind(wx.EVT_TEXT_ENTER,self.OnEnterPressed)  


        #***********************************************#
        box4 = wx.BoxSizer(wx.HORIZONTAL) 
        label4 = wx.StaticText(panel, -1, "只读取文本") 
        
        box4.Add(label4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t4 = wx.TextCtrl(panel, value = "只读文本",style = wx.TE_READONLY|wx.TE_CENTER) 
        # wx.TE_READONLY 文本将不可编辑

        box4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        box.Add(box4) 

        panel.SetSizer(box)
        # 创建并关联sizer到一个容器。
        # sizer被关联到容器使用wx.Window的SetSizer(sizer)方法。
        # 唯一的目的就是管理容器中的窗口部件的布局。
        # 只是一个屏幕布局的算法。

        self.Centre()
        self.Show()
        self.Fit() 

    def OnKeyTyped(self, event):
            print event.GetString()
            # 返回事件
            pass
    def PassWord(self, event):
            print "enter pressed"
            pass   
    def OnEnterPressed(self,event): 
            print "Enter pressed" 





app = wx.App()

mycoosk(None, "COOSK")

app.MainLoop()

        