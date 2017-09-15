# -*- coding: UTF-8 -*-

import wx

app = wx.App()

frame = wx.Frame(None, wx.ID_ANY, "COOSK" , size = (100,100))

panel = wx.Frame(frame)

label = wx.StaticText() 
# Wx.StaticText(parent, id, label, position, size, style)

frame.Show(True)

app.MainLoop()