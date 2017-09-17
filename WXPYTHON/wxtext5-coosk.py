# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,200))

        self.InitUI()
        # 调用函数 InitUI

    def InitUI(self):
        panel = wx.Panel(self)

        self.rb1 = wx.RadioButton(panel, 11, label = 'Value A', pos = (10,10), style = wx.RB_GROUP)
        # Wx.RadioButton(parent, id, label, pos, size, style) 
        # pos:一个wx.Point或一个Python元组，它是窗口部件的位置.
        # style参数仅用于该组中的第一个按钮。它的值是wx.RB_GROUP。
        # 对于组中的随后的按钮，wx.RB_SINGLE的style 参数可以任选地使用。
        # 11 = ID 
        self.rb2 = wx.RadioButton(panel, 22, label = 'Value B', pos = (10,40))
        self.rb3 = wx.RadioButton(panel, 33, label = 'Value C', pos = (10,70))
        self .Bind(wx.EVT_RADIOBOX,self.OnRadioBox)
        # 每任何组中的按钮被点击时 wx.RadioButton 事件绑定器 wx.EVT_RADIOBUTTON 触发相关的处理程序。

        labelList = ['Value X','Value Y','Value Z']

        self.rbox = wx.RadioBox(panel, label = 'RadioBox', pos = (80,10), choices = labelList)
        # Wx.RadioBox(parent, id, label, pos, size, choices[], initialdimensions, style)
        # wx.RadioBox 则以相互排斥的按钮集合在一个静态框。
        # RadioBox按钮将在按行或列的方式逐步布局。

        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)

        self.Centre()
        self.Show(True)

        pass

    def OnRadioBox():
        rb = e.GetEventObject() 
        print rb.GetLabel(),' is clicked from Radio Group' 
        pass

    def onRadioBox():
        print self.rbox.GetStringSelection(),' is clicked from Radio Box' 
        pass


app = wx.App()

mycoosk(None, "COOSK")

app.MainLoop()