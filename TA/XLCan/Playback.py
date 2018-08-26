#Read the receive file and achieve playback
import XLCanLib
import time
import ctypes

class playback():
    '''
    In this class we will achieve the playback
    '''

    ###############################
    def __init__(self,receiveFP):
    ###############################
        ''' Init the file '''
        
        self.receivePath = receiveFP
        self.receiveFP = open(self.receivePath,"r")
        self.id = []
        self.dlc = []
        self.data = []

    ##################
    def getCanMsg(self):
    ##################
        ''' In this function you will try to read the receive file and
        get all the msg like DLC, id, data and so on to prepare for the
        playback.'''
        
        for lines in self.receiveFP.readlines():
            self.id.append(lines[lines.find("id=") + 3:lines.find("l=") -1])
            self.dlc.append(lines[lines.find("l=") + 2:lines.find("l=") + 3])
            self.data.append(lines[lines.find("l=") + 5:lines.find("tid=") - 1])
        #print self.id,self.data
        self.receiveFP.close()

    ################
    def initCan(self):
    ################
        '''In this function, init CANlib'''
        try:
            self.can=XLCanLib.candriver()
            self.can.open_driver()
            self.mask=self.can.get_channel_mask()
            ok, self.phandle, self.pmask=self.can.open_port()
            print ok, self.phandle, self.pmask
            ok=self.can.activate_channel(self.phandle)
            print ok , "OK"
            if ok != 0:
                print "Can't activate channel"
                exit(0)
        except Exception as e:
            print "Error when can init" + str(e)

    ##################################        
    def tranEventMsg(self,canID,dlc,data):
    ##################################
        '''In this function transmit the event'''
        
        event_msg=XLCanLib.XLevent(0)
        event_msg.tag=XLCanLib.XL_TRANSMIT_MSG
        print hex(int(canID,16))
        event_msg.tagData.msg.id=(int(canID,16))
        event_msg.tagData.msg.flags=0
        event_msg.tagData.msg.dlc=int(dlc)
        for index in range(event_msg.tagData.msg.dlc):
            event_msg.tagData.msg.data[index] = int(data[2*index:2*(index+1)],16)
        '''
        if event_msg.tagData.msg.dlc == 4:
            event_msg.tagData.msg.data[0]=(int(data[0:2],16))
            event_msg.tagData.msg.data[1]=(int(data[2:4],16))
            event_msg.tagData.msg.data[2]=(int(data[4:6],16))
            event_msg.tagData.msg.data[3]=(int(data[6:8],16))
        elif event_msg.tagData.msg.dlc == 8:            
            event_msg.tagData.msg.data[0]=(int(data[0:2],16))
            event_msg.tagData.msg.data[1]=(int(data[2:4],16))
            event_msg.tagData.msg.data[2]=(int(data[4:6],16))
            event_msg.tagData.msg.data[3]=(int(data[6:8],16))
            event_msg.tagData.msg.data[4]=(int(data[8:10],16))
            event_msg.tagData.msg.data[5]=(int(data[10:12],16))
            event_msg.tagData.msg.data[6]=(int(data[12:14],16))
            event_msg.tagData.msg.data[7]=(int(data[14:16],16))
        '''

        #print event_msg.tagData.msg.data[7]
        event_count=ctypes.c_uint(1)
        ok=self.can.can_transmit(self.phandle, self.mask, event_count, event_msg)

    ###################
    def playBackMib(self):
    ###################
        '''
        In this function the receive will be read and acheive the playback
        step by step
        '''
        
        self.getCanMsg()
        self.initCan()
        print self.id
        for index in range(len(self.id)):
            self.tranEventMsg(self.id[index],self.dlc[index],self.data[index])
            time.sleep(0.02)

if __name__ == "__main__":
    filePath = r"D:\Temp\TA\XLCan\receive.txt"
    play = playback(filePath)
    #play.getCanMsg()
    play.playBackMib()
