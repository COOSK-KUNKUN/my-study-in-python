# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self, parent, title):
        super(mycoosk, self).__init__(parent, title = title, size = (300,400))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label = "Your choice:" ,style = wx.ALIGN_CENTRE)
        box.Add(self.label, 0 ,wx.EXPAND |wx.ALIGN_CENTER_HORIZONTAL |wx.ALL, 20)
        # wx.ALIGN_CENTER_HORIZONTAL 水平方向居中。

        cb1 = wx.StaticText(panel, label = "Combo box", style = wx.ALIGN_CENTRE)

        box.Add(cb1,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)

        dict = ['17GB','29KB','COOSK']
        self.combo= wx.ComboBox(panel,choices  = dict)
        # wx.ComboBox对象提供从项目选择列表。
        # 它可以被配置为一个下拉列表或永久性的显示。

        box.Add(self.combo,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        cb1 = wx.StaticText(panel,label = "Choice control",style = wx.ALIGN_CENTRE) 
        
        box.Add(cb1,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5) 
        self.choice = wx.Choice(panel,choices = dict) 
        # wx.Choice(parent, id, pos, size, n, choices[], style) 
        # 能使下拉表无法进行编辑
        # wx.Choice没有专门的样式，但是它有独特的命令事件：EVT_CHOICE。

        box.Add(self.choice,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5) 



        box.AddStretchSpacer()
        # box 加入伸张性空间

        self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

        panel.SetSizer(box)
        self.Centre()
        self.Show(True)

    def OnCombo(self,event):
        self.label.SetLabel('you selected' + self.combo.GetValue()+" from Combobox")
         

    def OnChoice(self,event):
        self.label.SetLabel("You selected "+ self.choice.GetString(self.choice.GetSelection())+" from Choice") 
        



app = wx.App()

mycoosk(None, "COOSK")

app.MainLoop()