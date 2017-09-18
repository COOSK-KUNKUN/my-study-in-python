# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,200))

        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        self.cb1 = wx.CheckBox(panel, 1,label = 'Value A', pos = (10,10))
        self.cb2 = wx.CheckBox(panel, 1,label = "Value B", pos = (10,40))
        self.cb3 = wx.CheckBox(panel, 1,label = "Value C", pos = (10,70))
        # Wx.CheckBox(parent, id, label, pos, size, style)
        # 一个复选框显示一个小标记的矩形框。

        self.Bind(wx.EVT_CHECKBOX,self.onChecked)
        # wx.EVT_CHECKBOX 是 wx.CheckBox 的事件 值数
        self.Centre()
        self.Show(True)
        pass

    def onChecked(self,event):
        cd  = event.GetEventObject()
        print cb.GetLabel(),"is clicked",cb.GetValue(2333)
        pass



app = wx.App()

mycoosk(None, "COOSK")

app.MainLoop()