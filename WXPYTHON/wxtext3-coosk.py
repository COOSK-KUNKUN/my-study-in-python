# -*- coding: UTF-8 -*-

import wx 
 
class Mycoosk(wx.Frame): 
   def __init__(self, parent, title): 
      super(Mycoosk, self).__init__(parent, title = title,size = (600,200))
      panel = wx.Panel(self) 
      box = wx.BoxSizer(wx.VERTICAL) 
      # Box：在一条水平或垂直线上的窗口部件的布局。通常用于嵌套的样式。
      # 当尺寸改变时，在控制窗口部件的的行为上很灵活。
      # 可用于几乎任何类型的布局。
      # 参数的值若是wx.HORIZONTAL或wx.VERTICAL，表示在水平或垂直方向居中。
      label = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
        
      txt1 = "good morning" 
      txt2 = "nice day" 
      txt3 = " eat good breakfast " 
      txt = txt1+"\n"+txt2+"\n"+txt3 
        
      font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
      label.SetFont(font) 
      label.SetLabel(txt) 
      #字体设置
      # SetFont(font)：项目的显示字体。类型是wx.Font。
      # SetLabel(txt)：项目的显示文本。
        
      box.Add(label,0,wx.ALIGN_CENTER) 
      lbl1 = wx.StaticText(panel,-1,style = wx.ALIGN_RIGHT)
      # TXT 中 txt3 的文本置于下一行的右边 
      txt = txt1+txt2+txt3 
        
      lbl1.SetLabel(txt) 
      lbl1.Wrap(200) 
      # textwrap.wrap(text[,width[, ...]])
      # 包装单个段落(text为输入，系字符串)，每行最长宽度width。
      # 返回输出行的列表，最后行无换行符。Width默认70。
      # 设置lbl1文本在box中的宽度
      box.Add(lbl1,0,wx.ALIGN_RIGHT)
      # 将lbl1的文本设置在右边 
        
      lbl2 = wx.StaticText(panel,-1, style = wx.ALIGN_CENTER | wx.ST_ELLIPSIZE_MIDDLE) 
      # wx.ST_ELLIPSIZE_MIDDLE  
      # 省略号(...)显示在中间，如果文本的大小大于标签尺寸
      lbl2.SetLabel(txt) 
      lbl2.SetForegroundColour((255,0,0)) 
      lbl2.SetBackgroundColour((0,0,0)) 
      # 设置lbl1中的文本样式（底部）
        
      font = self.GetFont() 
      lbl2.SetFont(font) 
        
      box.Add(lbl2,0,wx.ALIGN_CENTER) 
      panel.SetSizer(box) 
      self.Centre() 
      self.Show() 
        
app = wx.App() 
Mycoosk(None,  'COOSK') 
app.MainLoop()