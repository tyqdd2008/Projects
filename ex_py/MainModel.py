#!/usr/bin/env python
import os
import pprint
import random
import matplotlib
import numpy as np
import sys
import wx
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas,NavigationToolbar2WxAgg as NavigationToolbar
import pylab
#The main graphframe
class GraphFrame(wx.Frame):
	title = 'Demo: dynamic matplotlib graph'

	def __init__(self):
		#wx.Frame.__init__(self,None,-1,self.title,size = (500,300))
		wx.Frame.__init__(self,None,-1,self.title)

		self.paused = False
		self.create_menu()
		self.create_status_bar()
		self.create_main_panel()
		

	def create_menu(self):
		self.menubar = wx.MenuBar()

		menu_file = wx.Menu()
		m_expt = menu_file.Append(-1,"&Save plot\tCtrl-S","Save plot to file")
		self.Bind(wx.EVT_MENU,self.on_save_plot,m_expt)
		menu_file.AppendSeparator()
		m_exit = menu_file.Append(-1,"E&xit\tCtrl-X","Exit")
		self.Bind(wx.EVT_MENU,self.on_exit,m_exit)
		
		self.menubar.Append(menu_file,"&File")
		self.SetMenuBar(self.menubar)
#############create the main panel.It includes all the ctrl you need
	def create_main_panel(self):
		self.panel = wx.Panel(self)
	        self.file_getText = wx.TextCtrl(self.panel,-1,)	
                self.file_button = wx.Button(self.panel,-1,label = "OpenFile"''',size = ()''') 
                
		self.Bind(wx.EVT_BUTTON,self.on_file_button,self.file_button)
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                hbox.Add(self.file_getText,proportion = 0,flag = wx.LEFT,border = 10)
                hbox.Add(self.file_button,proportion = 0,flag = wx.LEFT,border = 10)

		self.init_plot()
		self.canvas = FigCanvas(self.panel,-1,self.fig)
                ##############how to eliminate the gap????There is a gap between hbox and vbox
	        hbox1 = wx.BoxSizer(wx.HORIZONTAL)	
                hbox1.Add(self.canvas,proportion = 1,flag = wx.ALL)
                vbox = wx.BoxSizer(wx.VERTICAL)    
                vbox.Add(hbox,proportion = 0,flag = wx.EXPAND)
                vbox.Add(hbox1,proportion = 1,flag = wx.LEFT|wx.TOP|wx.GROW)
		self.panel.SetSizer(vbox)
		vbox.Fit(self)
	
	def create_status_bar(self):
		self.statusbar = self.CreateStatusBar()
        
        def on_file_button(self,event):
                self.x = ginput(1)
                self.file_getText.AppendText(np.num2str(self.x))
                
############plot the figure to the FIGURE/Then use  FigCanvas to put figure to the panel
	def init_plot(self):
		self.dpi = 100
		self.fig = Figure((5.0,3.0),dpi = self.dpi)##set the w/h of the figure
#		self.fig = Figure(dpi = self.dpi)

                self.data = []####get the data
                self.data.append(np.arange(0,1,0.1))
                self.data.append(np.sin(self.data[0]))
               # import crash_on_ipy
		self.axes = self.fig.add_subplot(111)
		self.axes.set_axis_bgcolor('black')
		self.axes.set_title('Very important random data',size = 12)

		pylab.setp(self.axes.get_xticklabels(),fontsize = 8)
		pylab.setp(self.axes.get_yticklabels(),fontsize = 8)

		self.plot_data = self.axes.plot(self.data)###plot the data
               
      #  def draw_plot(self):
    #		self.plot_data.set_xdata(np.arange(len(self.data)))
#		self.plot_data.set_ydata(np.array(self.data))

#		self.canvas.draw()

    	def on_save_plot(self,event):
		file_choices = "PNG (*.png) | *.png"	

		dlg = wx.FileDialog(self,message = "Save plot as ...",defaultDir = os.getcwd(),defaultFile = "plot.png",wildcard = file_choices,style = wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.canvas.print_figure(path,dpi = self.dpi)
			self.flash_status_message("Saved to %s" % path)
	
	
	def on_exit(self,event):
		self.Destroy()
	
	def flash_status_message(self,msg,flash_len_ms = 1500):
		self.statusbar.SetStatusText(msg)
		self.timeroff = wx.Timer(self)
		sefl.Bind(wx.EVT_TIMER,self.on_flash_status_off,self.timeroff)
		self.timeroff.Start(flash_len_ms,oneShot = True)
	
	def on_flash_status_off(self,event):
		self.statusbar.SetStatusText('')

if __name__ == '__main__':
	app = wx.PySimpleApp()
	app.frame = GraphFrame()
	app.frame.Show()
	app.MainLoop()
