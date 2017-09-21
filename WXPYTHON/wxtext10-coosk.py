# -*- coding: UTF-8 -*-

import wx

class mycoosk(wx.Frame):
    """docstring for mycoosk"""
    def __init__(self,parent,title ):
        super(mycoosk, self).__init__(parent, title = title , size = (320,133) , )
        panel = wx.Panel(self)

        image = wx.Image("1.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # wx.Image(name, type=wx.BITMAP_TYPE_ANY, index=-1)
        # 从一个文件载入一个图像


        self.button = wx.BitmapButton(panel, -1,image, pos = (10,10),size=(70,70))
        self.Bind(wx.EVT_BUTTON,self.image,self.button)
        self.button.SetDefault()
        # 载入图片的窗口
    
    #***************************************************************************************#    
        self.Centre() 
        self.Show(True) 

    def image(self,event):
        print self.button.GetStringSelection(),' is clicked from button' 

 


app = wx.App()

mycoosk(None,"COOSK")

app.MainLoop()