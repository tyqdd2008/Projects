#!/usr/bin/env python
import wx
#import image

class ToolbarFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Toolbars',size = (300,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
#        toolbar.AddSimpleTool(wx.NewId(),images.GetNewBitmap(),"New","Long help")
        toolbar.Realize()
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(wx.NewId(),"Open","")
        menuBar.Append(menu1,"&File")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(),"&Copy","Copy in status bar")
        menu2.Append(wx.NewId(),"C&ub","")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(),"&Options","Display Options")
        menuBar.Append(menu2,"&Edit")
        self.SetMenuBar(menuBar)
if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = ToolbarFrame(parent = None,id = -1)
    frame.Show()
    app.MainLoop()


