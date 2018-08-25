#! /usr/bin/env python
import wx
class SketchWindow(wx.Window):
    def __init__(self,parent,ID):
        wx.Window.__init__(self,parent,ID)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color,self.thickness,wx.SOLID)#CREATE A wx.PenOBJECT
        self.lines = []
        self.curLine = []
        self.pos = (0,0)
        self.InitBuffer()

        #BIND EVENT 
        self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)
        self.Bind(wx.EVT_MOTION,self.OnMotion)
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.Bind(wx.EVT_IDLE,self.OnIdle)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
    def InitBuffer(self):
        size = self.GetClientSize()
        #CREATE DC
        self.buffer = wx.EmptyBitmap(size.width,size.height)
        dc = wx.BufferedDC(None,self.buffer)
        #USE DC
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        
        self.reInitBuffer = False
    
    def GetLinesData(self):
        return self.lines[:]
    def SetLinesData(self,lines):
        self.lines = lines[:]
        sel.InitBuffer()
        self.Refresh()

    def OnLeftDown(self,event):
        self.curLine = []
        self.pos = event.GetPositionTuple()#GET THE CURSOR POS
        self.CaptureMouse()#CATCH THE CURSOR
    
    def OnLeftUp(self,event):
        if self.HasCapture():
            self.lines.append((self.color,self.thickness,self.curLine))
            self.curLine = []
            self.ReleaseMouse()#REALEASE CURSOR

    def OnMotion(self,event):
        if event.Dragging() and event.LeftIsDown():#JUDGING IF THE MOUSE IS DRAGGING
            dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)#CREATE ANOTHER DC
            self.drawMotion(dc,event)
        event.Skip()

    #DRAW TO DC
    def drawMotion(self,dc,event):
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()
        coords = self.pos + newPos
        self.curLine.append(coords)
        dc.DrawLine(*coords)
        self.pos = newPos
    def OnSize(self,event):
        self.reInitBuffer = True #HANDLE RESIZE EVENT

    def OnIdle(self,event):#HANDLE IDLE EVENT
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)
    def OnPaint(self,event):
        dc = wx.BufferedPaintDC(self,self.buffer)#HANDLE DC

    # PAINT ALL LINES
    def DrawLines(self,dc):
        for colour,thickness,line in self.lines:
            pen = wx.Pen(colour,thickness,wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def SetColor(self,color):
        self.color = color
        self.pen = wx.Pen(self.color,self.thickness,wx.SOLID)
    def SetThickness(self,num):
        self.thicness = num
        self.pen = wx.Pen(self.color,self.thickness,wx.SOLID)

class SketchFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,-1,"Sketch Frame",size = (800,600))
        self.sketch = SketchWindow(self,-1)

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()













































