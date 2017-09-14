# -*- coding: UTF-8 -*-

import wx

class text(wx.Frame):
	"""docstring for text"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (300,200))
		self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
		self.Show(True)
# wx.TextCtrl 来声明一个简单的文本编辑器
# 因为在MyFrame.__init__ 中已经运行了self.Show()
# 所以在创建MyFrame的实例之后，就不用再调用frame.Show() 了。
# style值有：
# wx.TE_MULTILINE:文本控制显示多行
# wx.TE_RICH:用于windows，允许丰富文本样式的使用
# wx.TE_WORDWARP:以单词为界自动换行
# wx.HSCROLL:除非设置，否则不自动换行，并设置水平滚动条。

app = wx.App(False)

frame = text(None, 'COOSK')
app.MainLoop()
