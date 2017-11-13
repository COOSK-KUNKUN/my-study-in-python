# -*- coding: UTF-8 -*-

import wx
import math

class JSQ(wx.Frame):
    """docstring for JSQ"""
    def __init__(self, parent, title):
        super(JSQ, self).__init__(parent, title = title , size = (300,200))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        box_1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel , -1, '第一个数')
        box_1.Add(label, 1 ,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1 = wx.TextCtrl(panel)
        box_1.Add(self.t1, 1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1.Bind(wx.EVT_TEXT,self.OnKeyTyped)

        box.Add(box_1)


        box_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(panel, 1, '第二个数')
        box_2.Add(label_1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t2 = wx.TextCtrl(panel)
        box_2.Add(self.t2, 1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        box.Add(box_2)

        self.button_add = wx.Button()
        self.button_add.Bind()
        self.button_sub = wx.Button()
        self.button_add.Bind()
        self.Button_mul = wx.Button()
        self.button_add.Bind()
        self.Button_div = wx.Button()
        self.button_add.Bind()
        panel.SetSizer(box)
        self.Centre()
        self.Show(True)
        self.Fit()

    def OnKeyTyped(self, event):
        pass



app = wx.App()

JSQ(None,"COOSK")

app.MainLoop()