#! /usr/bin/env/python
import wx
import os
import pprint
import random
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas,NavigationToolbar2WxAgg as NavigationToolbar

class BarsFrame(wx.Frame):
        title = 'Demo: wxPython with matplotlib'
        def __init__(self):
		wx.Frame.__init__(self,None,-1,self.title)
		self.data = [5,6,9,14]
		self.create_menu()
		self.create_status_bar()
		self.create_main_panel()
		self.textbox.SetValue(''.join(map(str,self.data)))
		self.draw_figure()
	def create_menu(self):
		self.menubar = wx.MenuBar()
		menu_file = wx.Menu()
		m_expt = menu_file.Append(-1,"&Save plot\tCtrl-s","Save plot to file")
		self.Bind(wx.EVT_MENU,self.on_save_plot,m_expt)
		menu_file.AppendSeparator()
		m_exit = menu_file.Append(-1,"E&xit\tCtrl-X","Exit")
		self.Bind(wx.EVT_MENU,self.on_exit,m_exit)

		menu_help = wx.Menu()
		m_about = menu_help.Append(-1,"&About\tF1","About the demo")
		self.Bind(wx.EVT_MENU,self.on_about,m_about)

		self.menubar.Append(menu_file,"&File")
		self.menubar.Append(menu_help,"&Help")
		self.SetMenuBar(self.menubar)

	def create_main_panel(self):
		self.panel = wx.Panel(self)
		self.dpi = 100
		self.fig = Figure((5.0,4.0),dpi = self.dpi)
		self.canvas = FigCanvas(self.panel,-1,self.fig)
		self.axes = self.fig.add_subplot(111)
		self.canvas.mpl_connect('pick_event',self.on_pick)
		self.textbox = wx.TextCtrl(self.panel,size = (200,-1),style = wx.TE_PROCESS_ENTER)
		self.Bind(wx.EVT_TEXT_ENTER,self.on_text_enter,self.textbox)
		self.drawbutton = wx.Button(self.panel,-1,"Draw!")
		self.cb_grid = wx.CheckBox(self.panel,-1,"Show Grid",style = wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CHECKBOX,self.on_cb_grid,self.cb_grid)
		self.slider_label = wx.StaticText(self.panel,-1,"Bar width(%):")
		self.slider_width = wx.Slider(self.panel,-1,value = 20,minValue = 1,maxValue = 100,style = wx.SL_AUTOTICKS|wx.SL_LABELS)
		self.slider_width.SetTickFreq(10,1)
		self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK,self.on_slider_width,self.slider_width)
                self.toolbar = NavigationToolbar(self.canvas)
                self.vbox = wx.BoxSizer(wx.VERTICAL)
                self.vbox.Add(self.canvas,1,wx.LEFT | wx.TOP | wx.GROW)
                self.vbox.Add(self.toolbar,0,wx.EXPAND)
                self.vbox.AddSpacer(10)
                self.hbox = wx.BoxSizer(wx.HORIZONTAL)
                flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
                self.hbox.Add(self.textbox,0,border = 3,flag = flags)
                self.hbox.Add(self.drawbutton,0,border = 3,flag = flags)
                self.hbox.Add(self.cb_grid,0,border = 3,flag = flags)
                self.hbox.AddSpacer(30)
                self.hbox.Add(self.slider_label,0,flag  = flags)
                self.vbox.Add(self.hbox,0,flag = wx.ALIGN_LEFT | wx.TOP)

        def create_status_bar(self):
                self.statusbar = self.CreateStatusBar()
                
        def draw_figure(self):
                str  = self.textbox.GetValue()
                self.data = map(int,str.split())
                x = range(len(self.data))
                self.axes.clear()
                self.axes.grid(self.cb_grid.IsChecked())
                self.axes.bar(left = x,height = self.data,width = self.slider_width.GetValue() / 100.0,align = 'center',alpha = 0.44,picker = 5)
                self.canvas.draw()
        def on_cb_grid(self,event):
                self.draw_figure()
        def on_slider_width(self,event):
                self.draw_figure()
        def on_draw_button(self,event):
                self.draw_figure()
        def on_pick(self,event):
                box_points = event.artist_get_bbox().get_points()
                msg = "You've clicked on a bar with coords:\n %s" % box_points
                dlg = wx.MessageDialog(self,msg,"Click!",wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        def on_text_enter(self,event):
                self.draw_figure()
        def on_save_plot(self,event):
                file_choices  = "PNG(*.png) | .png"
                dlg = FileDialog(self,message = "Save plot as ...",defaultFile = "plot.png",wildcard = file_choices,style = wx.SAVE)
                if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                    self.canvas.print_figure(path,dpi = self.dpi)
                    self.flash_status_message("Saved to %s " % path)
        def on_exit(self,event):
                self.Destroy()
        def on_about(self,event):
                msg = """A demo using wxPython with matplotlib:"""
        def flash_status_message(self,msg,flash_len_ms = 1500):
                self.statusbar.SetSatusText(msg)
                self.timeroff = wx.Timer(self)
                self.Bind(wx.EVT_TIMER,self.on_flash_status_off,self.timeroff)
                self.timeroff.Start(flash_len_ms,oneShot = True)
        def on_flash_staus_off(self,event):
                self.statusbar.SetStatusText('')


if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = BarsFrame()
    app.frame.Show()
    app.MainLoop()














		




















