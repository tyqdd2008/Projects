#! /usr/bin/env python
import wx
from wx.lib.plot import PolyLine,PlotCanvas,PlotGraphics

class DataWxProcess(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,'DataWxProcess',size = (400,300))
		self.panel = wx.Panel(self,-1)
		#self.childPlotPanel = wx.Panel(self.panel,-1,size = (200,150))
		self.modelButton1 = wx.Button(self.panel,-1,size = (50,30),label = 'Model1')
		self.modelButton2 = wx.Button(self.panel,-1,size = (50,30),label = 'Model2')
		self.modelButton3 = wx.Button(self.panel,-1,size = (50,30),label = 'Model3')
		self.modelButton4 = wx.Button(self.panel,-1,size = (50,30),label = 'Model4')
		self.modelButton1.Bind(wx.EVT_BUTTON,self.OnButtonClick_Model1)	
		self.modelButton2.Bind(wx.EVT_BUTTON,self.OnButtonClick_Model2)	
		self.modelButton3.Bind(wx.EVT_BUTTON,self.OnButtonClick_Model3)	
		self.modelButton4.Bind(wx.EVT_BUTTON,self.OnButtonClick_Model4)	
		#self.canvas = PlotCanvas(self.childPlotPanel,id = -1,size = (200,150))
		self.canvas = PlotCanvas(self.panel,id = -1,size = (200,150))
		self.canvas.Draw(self.DrawBarGraph())
		hbox = wx.BoxSizer()
		#hbox.Add(self.childPlotPanel,proportion = 1,flag = wx.EXPAND)
		hbox.Add(self.modelButton1,proportion = 0)
		hbox.Add(self.modelButton2,proportion = 0)
		hbox.Add(self.modelButton3,proportion = 0)
		hbox.Add(self.modelButton4,proportion = 0)
#		hbox.Add(self.canvas,proportion = 2,flag = wx.EXPAND)
		self.panel.SetSizer(hbox)
	def OnButtonClick_Model1(self,event):
		pass
	def OnButtonClick_Model2(self,event):
		pass
	def OnButtonClick_Model3(self,event):
		pass
	def OnButtonClick_Model4(self,event):
		pass	
	def DrawBarGraph(self):
		points = [(1,0),(1,200)]
		line1 = PolyLine(points,colour = 'green',legend = 'Feb',width = 100)
		return PlotGraphics([line1],"Bar Graph - test","Months","Number of Students")




if __name__=='__main__':
	app = wx.PySimpleApp()
	frame = DataWxProcess()
	frame.Show()
	app.MainLoop()

