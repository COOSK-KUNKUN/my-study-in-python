# -*- coding: UTF-8 -*-

import wx

app = wx.App()
# 每一个 wxPython 应用程序都是一个 wx.App 实例。
# 对于大多数的简单程序，直接实例化 wx.App 即可。
# 但如果你希望创建一个复杂的应用程序，那么可以对 wx.App class 做一些扩展。
# ”False” 参数意味着“不要把 stdout 和 stderr 信息重定向到窗口”，
# 当然也可以不加 “False” 参数。

frame = wx.Frame(None, wx.ID_ANY, "COOSK", size = (400,300))
# 完整的语法是 wx.Frame(Parent, Id, Title)。
# 或 wx.Frame(Parent, ID, Title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name="frame")
# 使用 “None” 来表示这个frame是顶层的框架，没有父框架
# 使用 “wx.ID_ANY” 让 wxWidgets 来给我们挑选一个ID。
# ID 可以是任何数字。

panel = wx.Panel(frame)
# wx.Panel 对框架写入文本

label = wx.StaticText(panel, label = "hello wrold", pos = (100,100))

frame.Show(True)
# 显示这个Frame

app.MainLoop()
# 运行这个应用程序