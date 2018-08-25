#!/usr/bin/env python
import wx
class MenuEventFrame(wx.Frame):
    def _init_(self,parent,id):
        wx.Frame._init_(self,parent,id,'Menus',size = (300,200))
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuItem = menu1.Append(wx.NewId(),"&Exit")
        menuBar.Append(menu1,"&File")
        self.SetMenuBar(menuBar)

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = MenuEventFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()

