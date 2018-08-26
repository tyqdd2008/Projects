#! /usr/bin/python
 
# To change this template, choose Tools | Templates
# and open the template in the editor.
 
__author__="mapl"
__date__ ="$01.03.2010 14:04:51$"
 
import XLCanLib
import ctypes
import msvcrt
import time
 
 
if __name__ == "__main__":
    can=XLCanLib.candriver()
    can.open_driver()
    ok, p_hw_type, p_hw_index, p_hw_channel=can.get_appl_config()
    print ok, "appl config"
    ok=can.get_channel_index(hw_index=0, hw_channel=0)
    print ok, "channel_index"
    mask=can.get_channel_mask(hwindex=0, hwchannel=0)
    print mask, "mask"
    ok, phandle, pmask=can.open_port(access_mask=mask)
    print ok, mask, "open port"
    ok=can.can_set_channel_bitrate(phandle, mask, 500000)
    print ok, "ChannelBitrate"
    ok=can.activate_channel(phandle)
    print ok, phandle
    event_list=XLCanLib.XLevent(0)
    print event_list
    event_count=ctypes.c_uint(1)
    print event_count
    ok = 1
    loop=1
    fp = open(r"D:\Temp\TA\XLCan\receive.txt","w")
    while loop:
        if msvcrt.kbhit():
            loop=0
        ok=1
        while (ok):
            event_count=ctypes.c_uint(1)
            #print phandle, event_count
            ok=can.receive(phandle, event_count, event_list)
            time.sleep(0.001)
            #print ok, event_list
 
        rec_string=can.get_event_string(event_list)
        fp.write(rec_string)
        fp.write("\t\n")
        print rec_string
        #print ok, event_count, event_list
 
    can.deactivate_channel(phandle, mask)
    can.close_port(phandle)
    can.close_driver()
    fp.close()
