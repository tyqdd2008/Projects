#! /usr/bin/python
 
# To change this template, choose Tools | Templates
# and open the template in the editor.
 
__author__="mapl"
__date__ ="$03.03.2010 08:50:02$"
 
import XLCanLib
import ctypes
import msvcrt
import time
 
if __name__ == "__main__":
    can=XLCanLib.candriver()
    can.open_driver()
    mask=can.get_channel_mask()
    print mask, "mask"
    ok, phandle, pmask=can.open_port()
    print ok, phandle, pmask
    ok = can.get_channel_index()
    print ok, "channel index"
    #ok=can.can_set_channel_bitrate(phandle, mask, 500000)
    #print ok, "ChannelBitrate"
    ok, p_hw_type, p_hw_index, p_hw_channel=can.get_appl_config()
    print ok, p_hw_type, p_hw_index, p_hw_channel, "appl config"
    #ok=can.set_appl_config("xlCancontrol", 2, p_hw_type, p_hw_index, 1, 1)
    #print ok, "appl set config"
    ok=can.activate_channel(phandle)
    print ok, phandle
    event_msg=XLCanLib.XLevent(0)
    event_msg.tag=XLCanLib.XL_TRANSMIT_MSG
    event_msg.tagData.msg.id=0x9B000073
    print event_msg.tagData.msg.id, "event_msg.tagData.msg.id"
    event_msg.tagData.msg.flags=0
    event_msg.tagData.msg.dlc=8
    data = "7310040009000100"
    for index in range(event_msg.tagData.msg.dlc):
        event_msg.tagData.msg.data[index] = int(data[2*index:2*(index+1)],16)
   
    #print event_list
    event_count=ctypes.c_uint(1)
    print event_count
    ok = 1
    loop=1
    while loop:
        if msvcrt.kbhit():
            loop=0
            event_msg.tagData.msg.data[0]=0x73
            event_msg.tagData.msg.data[1]=0x10
            event_msg.tagData.msg.data[2]=0x04
            event_msg.tagData.msg.data[3]=0x00
            event_msg.tagData.msg.data[0]=0x09
            event_msg.tagData.msg.data[1]=0x00
            event_msg.tagData.msg.data[2]=0x01
            event_msg.tagData.msg.data[3]=0x00
            event_count=ctypes.c_uint(1)
            ok=can.can_transmit(phandle, mask, event_count, event_msg)
            print ok, event_msg, mask
            
        ok=1
        while (ok):
            time.sleep(0.1)
            event_count=ctypes.c_uint(1)
            ok=can.can_transmit(phandle, mask, event_count, event_msg)
            print ok, event_msg, mask
 
 
        #print ok, event_count, event_list
 
    can.deactivate_channel(phandle, mask)
    can.close_port(phandle)
    can.close_driver()
