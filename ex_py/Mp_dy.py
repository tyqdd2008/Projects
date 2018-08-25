#! /usr/bin/env/python
import os
import pprint
import random
import matplotlib
import numpy as np
import sys
import wx
import copy
matplotlib.use('WXAgg')
#from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas,NavigationToolbar2WxAgg as NavigationToolbar
#import pylab

#from pylab import *
import  matplotlib.pyplot as plt

global stress,strain,n_stress,n_strain
stress = {}
strain = {}
n_stress = []
n_strain = []
class GraphFrame(wx.Frame):
	title = 'Demo: dynamic matplotlib graph'

	def __init__(self):
		wx.Frame.__init__(self,None,-1,self.title,size = (600,-1),pos = (100,100))

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
	
	def create_main_panel(self):
		self.panel = wx.Panel(self)
		
		self.file_get_address = wx.TextCtrl(self.panel,-1,size = (300,-1))
		self.button_open_file = wx.Button(self.panel,-1,"OpenFile",size = (100,-1))
		
		self.Bind(wx.EVT_BUTTON,self.on_open_file,self.button_open_file)
		self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox1.Add(self.file_get_address,proportion = 0,border = 5,flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL)
		self.hbox1.AddSpacer(10)
		self.hbox1.Add(self.button_open_file,proportion = 1,border = 5,flag = wx.ALL)

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox.Add(self.hbox1,proportion = 0,flag = wx.ALL)
		
		self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.button_dynamic_model_math = wx.Button(self.panel,-1,"Dynamic Model Math",size = (200,-1))
                self.Bind(wx.EVT_BUTTON,self.on_Dynamic_Model_Math,self.button_dynamic_model_math)
		self.button_dynamic_model_dynamic = wx.Button(self.panel,-1,"Dynamic Model Dynamic",size = (200,-1))
		self.hbox2.Add(self.button_dynamic_model_math,proportion = 1,flag = wx.ALL)
		self.hbox1.AddSpacer(10)
		self.hbox2.Add(self.button_dynamic_model_dynamic,proportion = 1,flag = wx.ALL)
		
		self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.button_dynamic_model_kinetic = wx.Button(self.panel,-1,"Dynamic Model Kinetic",size = (200,-1))
		self.button_dynamic_model_grain_size = wx.Button(self.panel,-1,"Dynamic Model GrainSize",size = (200,-1))	
		self.hbox3.Add(self.button_dynamic_model_kinetic,proportion = 1,flag = wx.ALL)
		self.hbox1.AddSpacer(10)
		self.hbox3.Add(self.button_dynamic_model_grain_size,proportion = 1,flag = wx.ALL)
		self.vbox.Add(self.hbox2,proportion = 1,border = 5,flag = wx.ALL)
		self.vbox.AddSpacer(10)
		self.vbox.Add(self.hbox3,proportion = 1,border = 5,flag = wx.ALL)
		
		
		self.panel.SetSizer(self.vbox)
		self.vbox.Fit(self)

        def on_Dynamic_Model_Math(self,event):

        	Dynamic_Frame = Dynamic_Model_Math_Frame()
                Dynamic_Frame.Show()
                

	def on_open_file(self,event):

                global stress,strain,n_stress,n_strain

                dialogfile = wx.FileDialog(self,"Open File",os.getcwd(),style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST,wildcard = "*.txt")
                if dialogfile.ShowModal() == wx.ID_OK:
                    self.filepath = dialogfile.GetPath()
                    self.file_get_address.SetValue(self.filepath)
                dialogfile.Destroy()

                self.file_instruction = open(self.filepath,'r')
                self.instruction_filename = np.genfromtxt(self.file_instruction,delimiter = ',',unpack = True ,usecols = 0,dtype = 'S15',skip_header = 1) #Read the instruction file to get the filename
                
                self.file_instruction.close()
                self.file_instruction = open(self.filepath,'r')
                self.instruction_stress,self.instruction_strain = np.genfromtxt(self.file_instruction,usecols = (1,2),delimiter = ',',unpack = True,skip_header = 1)#Read the instruction file to get the instruction stress and strain
                self.file_instruction.close()
   #             print self.instruction_filename
             #   print self.instruction_stress,self.instruction_strain
            #    print self.data
                self.tmp_stress = copy.deepcopy(self.instruction_stress)
                self.tmp_strain = copy.deepcopy(self.instruction_strain)
                #self.instruction_stress.sort()
                self.tmp_strain.sort()
                self.tmp_stress.sort()
                self.n_stress = self.extract_data(self.tmp_stress)#extract the different stress
                self.n_strain = self.extract_data(self.tmp_strain)#extract the different strain
                n_stress = self.n_stress[:]
                n_strain = self.n_strain[:]
                index = self.filepath.rfind('/')
                self.readpath = self.filepath[0:index + 1]#extract the filepath /home/tarena/ex_py/
                print self.readpath
                self.ReadStress()
              #  self.ReadStrain()
                
                #print self.readpath
                #print self.instruction_stress,self.instruction_strain
                #E#print self.n_strain,self.n_stress
	def create_status_bar(self):
		self.statusbar = self.CreateStatusBar()
        def ReadStress(self):
                #First open file
               #
                global stress,strain
                global n_stress,n_strain

                for i_tmp_stress in n_stress:#Becauce stress is a mutiple dic so here we should initialize the dic
                    stress[i_tmp_stress] = {}
                for i_tmp_strain in n_stress:# The same as the stress
                    strain[i_tmp_strain] = {}
                for i_tmp_strain in range(0,len(self.instruction_strain)):
                
                    index = self.instruction_filename[i_tmp_strain].find(' ')
                    self.instruction_filename[i_tmp_strain] = self.instruction_filename[i_tmp_strain][:index]
                    self.readpath = self.readpath + self.instruction_filename[i_tmp_strain]
                    #print self.readpath
                    file_data = open(self.readpath,'r')
                    firstline_string = file_data.readline() 
                    index = self.readpath.rfind('/')
                    self.readpath = self.readpath[:index +1]
                    firstline_string = firstline_string.strip('\n')
                    firstline_string = firstline_string.split('\t')
                    for i_firstline in range(0,len(firstline_string)):
                        if firstline_string[i_firstline] == 'Strain':
                            i_strain = i_firstline
                        elif firstline_string[i_firstline] == 'Stress(MPa)':
                            i_stress = i_firstline
                    tmp_strain,tmp_stress = np.genfromtxt(file_data,usecols = (i_strain,i_stress),unpack = True)

                    import crash_on_ipy
                    stress[self.instruction_stress[i_tmp_strain]][self.instruction_strain[i_tmp_strain]] = tmp_stress
                    import crash_on_ipy
                    strain[self.instruction_stress[i_tmp_strain]][self.instruction_strain[i_tmp_strain]]= tmp_strain
                    #strain[self.instruction_stress[i_tmp_strain]] = {self.instruction_strain[i_tmp_strain]:tmp_strain}
                    file_data.close()
                #    print stress[self.instruction_stress[i_tmp_strain]],strain[self.instruction_stress[i_tmp_strain]] 
                #print stress[700][0.001],strain[900][0.001]

                          
        def extract_data(self,instruction_stress):
                self.n_tmp_stress = []
                self.n_tmp_stress.append(instruction_stress[0])
                self.i_tmp_stress = 0
                for self.i_stress in range(0,len(instruction_stress) - 1):#extract the different stress

                    if self.n_tmp_stress[self.i_tmp_stress] == instruction_stress[self.i_stress + 1]:
                        continue
                    else:
                        self.n_tmp_stress.append(instruction_stress[self.i_stress + 1])
                        self.i_tmp_stress += 1
                return self.n_tmp_stress
                

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

class Dynamic_Model_Math_Frame(wx.Frame):
        title = "Dynamic_Model_Math"

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
                global stress,strain,n_stress,n_strain

		self.panel = wx.Panel(self)
                self.temp_list = ['ALL']
                n_tmp = [str(j) for j in n_stress]
                print n_tmp
                for i in n_tmp :
                    self.temp_list.append(i)
                print self.temp_list
                self.radiobox = wx.RadioBox(self.panel,-1,"A Radio Box",(10,10),wx.DefaultSize,self.temp_list,1,wx.RA_SPECIFY_ROWS) 
		self.Bind(wx.EVT_RADIOBOX,self.on_temp_chose,self.radiobox)
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                hbox.Add(self.radiobox,proportion = 0,flag = wx.LEFT,border = 10)

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
        
        def on_temp_chose(self,event):
            #    self.init_plot()
#		self.canvas = FigCanvas(self.panel,-1,self.fig)
            #    self.x = self.fig.ginput(1)
            #    print self.x
           #     cid = self.canvas.mpl_connect('button_press_event',self.on_pick)
                
                self.axes_cid = self.canvas.mpl_connect('axes_enter_event',self.on_axes_enter)
                
                self.axes_levave_cid = self.canvas.mpl_connect('axes_leave_event',self.on_axes_leave)
              #  self.file_getText.AppendText(np.num2str(self.x))
                
############plot the figure to the FIGURE/Then use  FigCanvas to put figure to the panel
        def on_axes_enter(self,event):
                
                cid = self.canvas.mpl_connect('button_press_event',self.on_pick)
        def on_axes_leave(self,event):
                self.canvas.mpl_disconnect(self.axes_cid)
                self.canvas.mpl_disconnect(self.axes_leave_cid)
        def on_pick(self,event):
                print 'x = %f,y = %f'%(event.xdata,event.ydata)
	def init_plot(self):
                global stress,strain,n_stress,n_strain 
		self.dpi = 100
		#self.fig = plt.figure((5.0,3.0),dpi = self.dpi)##set the w/h of the figure
                num_tmp = len(n_stress)
                num_strain = len(n_strain)
		self.fig = plt.figure()##set the w/h of the figure
#		self.fig = Figure(dpi = self.dpi)

        #        self.data = []####get the data
        #        self.data.append(np.arange(0,1,0.1))
        #        self.data.append(np.sin(self.data[0]))
               # import crash_on_ipy
                self.plot_data = []
                print n_stress,n_strain
                for i_tmp in range(0,len(n_stress)):

                    self.axes = self.fig.add_subplot(1,num_tmp,i_tmp)
                    self.axes.set_axis_bgcolor('black')
                    self.axes.set_title('Very important random data',size = 12)

                    for i_strain in n_strain:
                        #pylab.setp(self.axes.get_xticklabels(),fontsize = 8)
                        #pylab.setp(self.axes.get_yticklabels(),fontsize = 8)
                        print i_tmp
                        self.axes.plot(strain[n_stress[i_tmp]][i_strain],stress[n_stress[i_tmp]][i_strain])###plot the data
                        import crash_on_ipy
                 
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



