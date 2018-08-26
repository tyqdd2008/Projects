import cv2
import os
import numpy as np
import ctypes
import threading
import datetime
from time import *
EDAS_Dir = r"D:\__AAMU_RUNTIME__\__PyScripts__\PyEDAS"
TmpDir = r"D:\Temp\TA\MGB\SaveImage"
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
class PyMGB(object):
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #==========================================
    def __init__(self, isVirtual=0, Display = "Top", VirtualMKV_FN=None, Virtual_IMG_FN=None, DecodeFramerate=None):
    #==========================================
        super(PyMGB, self).__init__()
        
        if Display == "Top":
            IP="192.168.1.200"
            Port="50000"
        elif Display == "Bottom":
            IP="192.168.1.201"
            Port="50050"
        elif Display == "Test":
            IP="localhost"
            Port="1883"
        else: assert 0
        
    
        # CHANGE HERE -------------------------------------------------
        self.Input_FN = "tcp://" + IP + ":" + Port
        DLL_PureFN = "libMPEGTS_Decoder.dll"
        self.libMGB_FN = EDAS_Dir + "/PyMGB/Lib/Windows/" + DLL_PureFN #change path to PyMGB when changing directory
        #self.libMGB_FN = EDAS_Dir + "/PyMGB/Lib/Windows/" + DLL_PureFN
        self.verbose = 1
        # -------------------------------------------------------------
        #printLARGE("MGB INIT", 2)
        
        self.isVirtual = isVirtual
        self.CurFrame = None
        self.InternalImgData = None
        self.Lock_CurFrame = threading.Lock()
        self.FrameCnt = 0
        self.isRunning = False
        self.doLoop = True
        
        if isVirtual == 1: #load from M2TS / MKV
            print "MGB: Virtual Mode"
            self.libMGB = None
            if VirtualMKV_FN == None:
                if Display == "Top":
                    self.Input_FN = EDAS_Dir + r"\PyMGB\TestVideo_MediaPlayback.mkv"
                    
                elif Display == "Bottom":
                    print "WARNING: Missing testvideo for Bottom Display"
                    self.Input_FN = EDAS_Dir + r"\PyMGB\TestVideo_MediaPlayback.mkv"
                    
                else: 
                    assert 0
                assert exists(self.Input_FN)
            else: 
                self.Input_FN = VirtualMKV_FN
                assert exists(self.Input_FN)
                
        if isVirtual == 2: #load an image as permanent 
            assert exists(Virtual_IMG_FN)
            self.PermanentScreen = readImg(Virtual_IMG_FN)
            self.libMGB = None
            return # avoid stuff below


        #need to add to PATH, otherwise DLL is not found
        os.environ['PATH'] = os.path.dirname(self.libMGB_FN) + ';' + os.environ['PATH']
        
        print "Loading:", self.libMGB_FN
        print "Input:", self.Input_FN
        self.libMGB=ctypes.cdll.LoadLibrary(self.libMGB_FN)
        self.data_Size = ctypes.c_int(0)
        self.height = ctypes.c_int(0)
        self.width = ctypes.c_int(0)
        self.StreamFPS = ctypes.c_double(0.0)
        self.linesize0 = ctypes.c_int(0)
        self.linesize1 = ctypes.c_int(0)
        self.linesize2 = ctypes.c_int(0)
        self.system = ctypes.c_int(0)
        self.id = ctypes.c_int(0)
        self.frame_id = ctypes.c_int64(0)   #c_int64 necessary. standard c_int is only int32 and to small for returned number 

		
        self.decodeErrors = 0
        self.decodeFramerate = DecodeFramerate
        self.index = 0
        
        self.PyMGB_Name = "PyMGB"
        
        self.id.value = self.libMGB.Init_Decoder_YUV(ctypes.addressof(self.data_Size), 
                                       ctypes.addressof(self.linesize0), 
                                       ctypes.addressof(self.linesize1), 
                                       ctypes.addressof(self.linesize2), 
                                       ctypes.addressof(self.height), 
                                       ctypes.addressof(self.width),
                                       self.Input_FN, 
                                       ctypes.addressof(self.StreamFPS), 
                                       self.system)
        
        print "Init_Decoder_YUV() returned: ", self.id.value
        
        self.DimX = self.width.value
        self.DimY = self.height.value
        
        assert self.id.value != -1
        
        self.PyMGB_Name = "PyMGB{}: ".format(self.id.value)
        print "PyMGB has ID: ", self.id.value
        
        if not self.decodeFramerate:
            self.decodeFramerate = self.StreamFPS.value
        
        print self.PyMGB_Name + "Returned width:", self.DimX, "height:", self.DimY
        print self.PyMGB_Name + "Returned line sizes:"
        print self.PyMGB_Name + "ls0:", self.linesize0.value
        print self.PyMGB_Name + "ls1:", self.linesize1.value
        print self.PyMGB_Name + "ls2:", self.linesize2.value
        
        print self.PyMGB_Name + "Data size of one frame is: {} bytes\n".format(self.data_Size.value)
        print self.PyMGB_Name + "FPS from Inputfile: {}".format(self.StreamFPS.value)
        
        
        
        #DataBufTyp=ctypes.c_char*self.data_Size.value
        #DataBuf=DataBufTyp()


        
    #==========================================
    def __del__(self):
    #==========================================
        #if self.isRunning == True:
        #    self.stopGrabbing()
            
        if self.libMGB != None: # virtual mode
            if self.libMGB.Deinit_Decoder(self.id) == 0:
                print self.PyMGB_Name + "Decoder is deinitialized"      
            else: 
                print  self.PyMGB_Name + "ERROR: Decoder could not deinitialize"
        
    #==========================================
    def startGrabbing(self):
    #==========================================
        #-------------------------------------
        # COMMENT
        #-------------------------------------
        if self.isRunning == True:
            print self.PyMGB_Name + "Grabbing already running"
            return None
        
        print self.PyMGB_Name + "startGrabbing()"
        self.isRunning = True
        
        if self.isVirtual == 2: #extra debug mode: permanent screen
            return #do not start thread
        
        args = tuple()
        self.terminateThread = False
        MyThread = threading.Thread(target=self.decode_WithThread, args=args)
        MyThread.daemon = True # OK for main to exit when instance is still running, BUT we at least try by the terminate flag
        print self.PyMGB_Name + "Starting decode_WithThread()"
        MyThread.start()
        
        #give it some time to deliver...
        while self.InternalImgData is None:
            print self.PyMGB_Name + "Waiting for decoded image data..."
            sleep(0.3)
    
    #==========================================
    def saveCurrentFrame(self, Desc="GrabbedSingleFrame"):
    #==========================================            
        ImgBGR = self.getCurrentFrame()
        #ImgFN = "./PyMGB_%05d.jpg" % self.FrameCnt
        TS = datetime.datetime.now()
        self.ImgFN = TmpDir + "/%s %s.png" % (Desc, TS.strftime("%Y_%m_%d__%H_%M_%S_%f") )
        cv2.imwrite(self.ImgFN, ImgBGR)
        print self.PyMGB_Name + "Saved current frame to: ", self.ImgFN

    #==========================================
    def stopGrabbing(self):
    #==========================================
        print self.PyMGB_Name + "stopGrabbing()"
        self.terminateThread = True
        self.isRunning = False
        sleep(2) #give some time to finish
        
    #==========================================
    def getCurrentFrame(self):
    #==========================================
        
        if self.isVirtual == 2: #extra debug mode: permanent screen
            return self.PermanentScreen
    
        #print "MGB: getCurrentFrame()"
        self.Lock_CurFrame.acquire()
        assert not self.InternalImgData is None
        ImgYUV = np.reshape(self.InternalImgData, (int(self.height.value*1.5),self.width.value))
        ImgBGR=cv2.cvtColor(ImgYUV, cv2.COLOR_YUV420p2RGB, cv2.CV_8UC3)
        assert ImgBGR.shape[:2] == (self.DimY, self.DimX)
        self.Lock_CurFrame.release()
        return ImgBGR
    
    #==========================================
    def get_YUV(self):
    #==========================================
        assert self.isVirtual != 2
        
        self.Lock_CurFrame.acquire()
        assert not self.InternalImgData is None
        YUV420 = np.reshape(self.InternalImgData, (int(self.height.value*1.5),self.width.value))
        self.Lock_CurFrame.release()
        Y1 = YUV420.shape[0] / 3 * 2 # LUM
        Y2 = YUV420.shape[0] / 3 / 2 # U Double
        Y3 = YUV420.shape[0] / 3 / 2 # U Double
        
        VertStep = YUV420.shape[0] / 3 / 2        
        Y = YUV420[0 : Y1, :]
        U = YUV420[Y1: Y1 + Y2, :]
        U = np.reshape(U, (Y2*2, YUV420.shape[1] / 2))
        V = YUV420[Y1+Y2:, :]
        V = np.reshape(V, (Y2*2, YUV420.shape[1] / 2))

        U = cv2.resize(U, (YUV420.shape[1], Y1), interpolation=cv2.INTER_LINEAR)
        V = cv2.resize(V, (YUV420.shape[1], Y1), interpolation=cv2.INTER_LINEAR)
        YUV = np.dstack((Y, U, V))
        
        return YUV
    
#         YUV_444 = cv2.cvtColor(ImgBGR, cv2.COLOR_RGB2YUV, cv2.CV_8UC3)
#         return YUV_444
    
    #==========================================
    def get_Y(self):
    #==========================================
        YUV= self.get_YUV()
        return YUV[:,:,0]        


    
# #==========================================
# def resizeToWidth(Img, Width, Interp=cv2.INTER_LINEAR):
# #==========================================
#     (rows, cols) = Img.shape[:2]
#     RatioX = float(cols)/Width;
#     Height = int(rows/RatioX);
#     return cv2.resize(Img, (Width, Height), interpolation=Interp)
            
    
    #==========================================
    def decode_SingleFrame_YUV(self):
    #==========================================
        
        assert self.isVirtual != 2 #not yet implemented!
        
        assert not self.isRunning, self.PyMGB_Name + "Not permitted when real-time grabbing is active"
        ImgData = self.decode_ImgData()
        ImgYUV_420 = np.reshape(ImgData, (int(self.height.value*1.5),self.width.value))
        ImgBGR     = cv2.cvtColor(ImgYUV_420, cv2.COLOR_YUV420p2RGB, cv2.CV_8UC3)
        #TBD: BAD! But OpenCV lacks direct conversion. Optimize by direct rescale.
        ImgYUV_444 = cv2.cvtColor(ImgBGR, cv2.COLOR_RGB2YUV, cv2.CV_8UC3) #strange: "RGB"
        return ImgYUV_444
    
    #==========================================
    def skipFrames(self, NumFrames):
    #==========================================
        
        assert self.isVirtual == 1 and not self.isRunning
        SkippedIDs = []
        for i in range(0, NumFrames):
            ImgData = self.decode_ImgData()
            ImgID   = self.frame_id
            # JUST UNROLL THE VIDEO, DISCARD FRAMES
            SkippedIDs.append(ImgID)
        return SkippedIDs
            
    
    #==========================================
    def decode_SingleFrame_BGR(self):
    #==========================================
        #assert not self.isRunning, "Not permitted when real-time grabbing is active"
        
        assert self.isVirtual != 2 #not yet implemented!
        
        if not self.isRunning: #step-by-step decoding
            ImgData = self.decode_ImgData()
            ImgID   = self.frame_id
            if ImgData is None: # probably end of file, and looping disabled
                print "Warning: ImgData == None"
                return None, None, None
            #assert not ImgData is None
            ImgTS = datetime.datetime.now()
            ImgYUV = np.reshape(ImgData, (int(self.height.value*1.5),self.width.value))
            ImgBGR=cv2.cvtColor(ImgYUV, cv2.COLOR_YUV420p2RGB, cv2.CV_8UC3) #strange: "RGB"
        else: #max-speed decoding
            self.Lock_CurFrame.acquire()
            #assert not self.InternalImgData is None
            if self.InternalImgData is None: # probably end of file, and looping disabled
                print "Warning: ImgData == None"
                return None, None, None
            
            ImgTS = datetime.datetime.now()
            ImgID   = self.frame_id
            ImgYUV = np.reshape(self.InternalImgData, (int(self.height.value*1.5),self.width.value))
            ImgBGR=cv2.cvtColor(ImgYUV, cv2.COLOR_YUV420p2RGB, cv2.CV_8UC3)
            self.Lock_CurFrame.release()        
        return ImgBGR, ImgTS, ImgID
    
    #==========================================
    def decode_ImgData(self):
    #==========================================
        data_buf_y = ctypes.c_char * (self.linesize0.value * self.height.value)
        data_buf_u = ctypes.c_char * (self.linesize1.value * self.height.value / 2)
        data_buf_v = ctypes.c_char * (self.linesize2.value * self.height.value / 2)
        data_y = data_buf_y()
        data_u = data_buf_u()
        data_v = data_buf_v()
        
        self.index += 1
        #print "get_frame", self.index
    
        ret = self.libMGB.Get_Frame_YUV(self.id,
                                    ctypes.byref(data_y), 
                                    ctypes.byref(data_u), 
                                    ctypes.byref(data_v), 
                                    self.data_Size, 
                                    ctypes.addressof(self.height), 
                                    ctypes.addressof(self.width),
                                    ctypes.addressof(self.frame_id) )
        #print "Frame ID: ", self.frame_id.value
        #print "PyMGB with ID:", self.id.value, "get_frame done with", ret
        
        #if self.verbose:
        #    print "Get_Frame_YUV() returned: ", ret
        
        #===============================================================
        # Reinitialisierung bei virtual MGB, falls das Video zu Ende ist 
        if ret == 0 and self.doLoop:
            if (self.decodeErrors) % 10 == 1: 
                print "WARNING: MGB: decoding errors (Num: %d)" % self.decodeErrors
            self.decodeErrors += 1
            if self.decodeErrors > 50 and self.isVirtual:    
                self.reintializingVideoStream()
                self.decodeErrors = 0
            if self.decodeErrors > 60 and not self.isVirtual:    
                self.reintializingVideoStream()
                self.decodeErrors = 0
        #===============================================================
        
        if ret == 0 and not self.doLoop:
            return None
        
        ImgDataY = np.frombuffer(data_y, np.uint8)
        ImgDataU = np.frombuffer(data_u, np.uint8)
        ImgDataV = np.frombuffer(data_v, np.uint8)
        ImgData = np.array(ImgDataY)
        ImgData = np.append(ImgData, ImgDataU, 0)
        ImgData = np.append(ImgData, ImgDataV, 0)
        return ImgData

    #==========================================
    def decode_WithThread(self):
    #==========================================
        print self.PyMGB_Name + "concurrently starting decode_WithThread()"
        #for i in range(1000):
        
        SavedInternalCounter = 0
        start_time = datetime.datetime.now()
        print self.PyMGB_Name + "decode framerate is:", self.decodeFramerate
        
        while 1:
            if self.terminateThread:
                break
            
            ts = datetime.datetime.now()
            
        
            ImgData = self.decode_ImgData()
            #time.sleep(0.2) #HACK!!
            #print "DECODED"
            
            self.FrameCnt += 1

            #==================================================================
            #Reduzierung der Framerate zum speichern in InternalData
            if self.FrameCnt % (self.StreamFPS.value / float(self.decodeFramerate)) < 1:     #An dieser Stelle gewollt oder in Zeile 260?
                self.Lock_CurFrame.acquire()
                self.InternalImgData = ImgData
                SavedInternalCounter += 1
                self.Lock_CurFrame.release()
            #==================================================================
                    
                if 0: #debug
                    if i % 100 == 0:
                        ImgYUV = np.reshape(self.InternalImgData, (int(self.height.value*1.5),self.width.value))     
                        ImgFN = "./Testframe_%d.jpg" % self.FrameCnt    #ts.strftime("%Y_%m_%d__%H_%M_%S_%f")
                        ImgBGR=cv2.cvtColor(ImgYUV, cv2.COLOR_YUV420p2RGB, cv2.CV_8UC3)
                        cv2.imwrite(ImgFN, ImgBGR)
                        SavedInternalCounter += 1
                        #sleep(0.09) #Simulate imwrite
                        #print "Written: ", ImgFN
                        
                #sleep(1.0/50)
                
            #==============================================================================
            if self.isVirtual:
                while 1:
                    if (datetime.datetime.now() - ts).total_seconds() >= (1 / self.StreamFPS.value):
                        break
                    time.sleep(0.001)
            #==================================================================
            
        #Debug variables
        stop_time = datetime.datetime.now()
        fps = SavedInternalCounter / (stop_time - start_time).total_seconds()
        decodeFps = self.FrameCnt / (stop_time - start_time).total_seconds()
        print(self.PyMGB_Name + "Average FPS saved in InternalData: {}\n".format(fps))
        print(self.PyMGB_Name + "Average Decode-FPS: {}\n".format(decodeFps))
        
        print self.PyMGB_Name + "decode_WithThread() finished"
        #flush()
        
        
    #===============================================            
    def reintializingVideoStream(self):
    #===============================================
        #assert not self.isVirtual:
        
        print self.PyMGB_Name + "Reinitializing video stream"
        ret = self.libMGB.Deinit_Decoder(self.id)
        print self.PyMGB_Name + "Deinitalizing Decoder returned:", ret
        assert ret is 0
        
        self.id.value = self.libMGB.Init_Decoder_YUV(ctypes.addressof(self.data_Size), 
                                   ctypes.addressof(self.linesize0), 
                                   ctypes.addressof(self.linesize1), 
                                   ctypes.addressof(self.linesize2), 
                                   ctypes.addressof(self.height), 
                                   ctypes.addressof(self.width),
                                   self.Input_FN, 
                                   ctypes.addressof(self.StreamFPS), 
                                   self.system)
        print self.PyMGB_Name + "Init_Decoder_YUV() returned: ", self.id.value
        print self.PyMGB_Name + "Rename PyMGB to new Decoder ID ", self.id.value
        self.PyMGB_Name = "PyMGB{}: ".format(self.id.value)
        
        assert ret != -1
        print self.PyMGB_Name + "Reinitializing completed"

if __name__ == "__main__":
    MGB = PyMGB(isVirtual=False)
    MGB.startGrabbing()
    MGB.saveCurrentFrame()
    MGB.stopGrabbing()

