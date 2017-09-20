# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,400))

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        box =  wx.BoxSizer(wx.VERTICAL)

        self.sld = wx.Slider(panel, value = 10, minValue = 1, maxValue = 100, style = wx.SL_VERTICAL|wx.SL_LABELS)
        # wx.SL_VERTICAL 水直滑块
        # wx.SL_LABELS 显示最小值，最大值，和当前值


        box.Add(self.sld, 1, flag = wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border = 20)
        self.sld.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        panel.SetSizer(box) 
        self.Centre() 
        self.Show(True)      


        pass

    def OnSliderScroll(self,event):
        obj = event.GetEventObject() 
        val = obj.GetValue() 
            

app = wx.App()

mycoosk(None , "COOSK")

app.MainLoop()