# To change this template, choose Tools | Templates
# and open the template in the editor.
 
import ctypes
 
XLuint64=ctypes.c_ulonglong
XLaccess=XLuint64
XLstatus=ctypes.c_short
XLporthandle=ctypes.c_long
 
XL_HWTYPE_NONE=0
XL_ACTIVATE_RESET_CLOCK=8
#XL_HWTYPE_CANCARDXL=15
XL_HWTYPE_CANCASEXL=21
 
XL_BUS_TYPE_NONE=0
XL_BUS_TYPE_CAN=1
 
XL_INTERFACE_VERSION=3
 
XL_INVALID_PORTHANDLE=-1
 
XL_ACTIVATE_NONE=0
XL_ACTIVATE_RESET_CLOCK=8
 
XLeventtag=ctypes.c_ubyte
MAX_MSG_LEN=8
 
XL_NO_COMMAND               = 0
XL_RECEIVE_MSG              = 1
XL_CHIP_STATE               = 4
XL_TRANSCEIVER              = 6
XL_TIMER                    = 8
XL_TRANSMIT_MSG             =10
XL_SYNC_PULSE               =11
XL_APPLICATION_NOTIFICATION =15
 
#//for LIN we have special events
XL_LIN_MSG                  =20
XL_LIN_ERRMSG               =21
XL_LIN_SYNCERR              =22
XL_LIN_NOANS                =23
XL_LIN_WAKEUP               =24
XL_LIN_SLEEP                =25
XL_LIN_CRCINFO              =26
 
#// for D/A IO bus
XL_RECEIVE_DAIO_DATA        =32
 
class s_xl_can_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong),
                ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort),
                ("res1", XLuint64),
                ("data", ctypes.c_ubyte*MAX_MSG_LEN)]
 
class s_xl_chip_state(ctypes.Structure):
    _fields_ = [("busStatus", ctypes.c_ubyte),
                ("txErrorCounter", ctypes.c_ubyte),
                ("rxErrorCounter", ctypes.c_ubyte),
                ("chipStatte", ctypes.c_ubyte),
                ("flags", ctypes.c_uint)]
 
class s_xl_lin_crc_info(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("flags", ctypes.c_ubyte)]
 
class s_xl_lin_wake_up(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]
 
class s_xl_lin_no_ans(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte)]    #
 
class s_xl_lin_sleep(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]
 
class s_xl_lin_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("dlc", ctypes.c_ubyte),
                ("flags", ctypes.c_ushort),
                ("data", ctypes.c_ubyte*8),
                ("crc", ctypes.c_ubyte)]
 
class s_xl_lin_msg_api(ctypes.Union):
    _fields_ = [("s_xl_lin_msg", s_xl_lin_msg),
                ("s_xl_lin_no_ans", s_xl_lin_no_ans),
                ("s_xl_lin_wake_up", s_xl_lin_wake_up),
                ("s_xl_lin_sleep", s_xl_lin_sleep),
                ("s_xl_lin_crc_info", s_xl_lin_crc_info)]
 
class s_xl_sync_pulse(ctypes.Structure):
    _fields_ = [("pulseCode", ctypes.c_ubyte),
                ("time", XLuint64)]
 
class s_xl_daio_data(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_ubyte),
                ("timestamp_correction", ctypes.c_uint),
                ("mask_digital", ctypes.c_ubyte),
                ("value_digital", ctypes.c_ubyte),
                ("mask_analog", ctypes.c_ubyte),
                ("reserved", ctypes.c_ubyte),
                ("value_analog", ctypes.c_ubyte*4),
                ("pwm_frequency", ctypes.c_uint),
                ("pwm_value", ctypes.c_ubyte),
                ("reserved1", ctypes.c_uint),
                ("reserved2", ctypes.c_uint)]
 
class s_xl_transceiver(ctypes.Structure):
    _fields_ = [("event_reason", ctypes.c_ubyte),
                ("is_present", ctypes.c_ubyte)]
 
class s_xl_tag_data(ctypes.Union):
    _fields_ = [("msg", s_xl_can_msg),
                ("chipState", s_xl_chip_state),
                ("linMsgApi", s_xl_lin_msg_api),
                ("syncPulse", s_xl_sync_pulse),
                ("daioData", s_xl_daio_data),
                ("transceiver", s_xl_transceiver)]
 
class s_xl_event(ctypes.Structure):
    _fields_ =[ ("tag", XLeventtag),
                ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort),
                ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort),
                ("timeStamp", XLuint64),
                ("tagData", s_xl_tag_data)]
 
XLevent=s_xl_event
 
class candriver():
 
    def __init__(self):
        self.candll=ctypes.windll.LoadLibrary("vxlapi.dll")
         
    def open_driver(self):
         
        ok = self.candll.xlOpenDriver()
        return ok
     
    def get_appl_config(self, appname="xlCANcontrol", channel=2, bustype=XL_BUS_TYPE_CAN):
        app_name=ctypes.c_char_p(appname)
        app_channel=ctypes.c_uint(channel)
        p_hw_type=ctypes.pointer(ctypes.c_uint())
        p_hw_index=ctypes.pointer(ctypes.c_uint())
        p_hw_channel=ctypes.pointer(ctypes.c_uint())
        bus_type=ctypes.c_uint(bustype)
        ok=self.candll.xlGetApplConfig(app_name, app_channel, p_hw_type, p_hw_index, p_hw_channel, bus_type)
        return ok, p_hw_type.contents, p_hw_index.contents, p_hw_channel.contents
 
    def set_appl_config(self, appname, appchannel, hwtype, hwindex,  hwchannel, bustype):
        self.candll.xlSetApplConfig.argtypes=[ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok=self.candll.xlSetApplConfig(appname, appchannel, hwtype, hwindex, hwchannel, bustype)
        return ok
         
    def get_channel_index(self, hw_type=XL_HWTYPE_CANCASEXL, hw_index=0, hw_channel=0):
 
        self.candll.xlGetChannelIndex.argtypes=[ctypes.c_int, ctypes.c_int, ctypes.c_int]
        channel_index=self.candll.xlGetChannelIndex(hw_type, hw_index, hw_channel)
        return channel_index
 
    def get_channel_mask(self, hwtype=XL_HWTYPE_CANCASEXL, hwindex=0, hwchannel=0):
        self.candll.xlGetChannelMask.argtypes=[ctypes.c_int, ctypes.c_int, ctypes.c_int]
        mask=self.candll.xlGetChannelMask(hwtype, hwindex, hwchannel)
        return ctypes.c_ulonglong(mask)
 
    def open_port(self, port_handle=XLporthandle(XL_INVALID_PORTHANDLE), user_name="xlCANcontrol", access_mask=XLaccess(1), permission_mask=XLaccess(1), rx_queue_size=1024, interface_version=XL_INTERFACE_VERSION, bus_type=XL_BUS_TYPE_CAN):
        self.candll.xlOpenPort.argtypes=[ctypes.POINTER(XLporthandle), ctypes.c_char_p, XLaccess, ctypes.POINTER(XLaccess), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok=self.candll.xlOpenPort(port_handle, user_name, access_mask, permission_mask, rx_queue_size, interface_version, bus_type)
        return ok, port_handle, permission_mask
 
    def activate_channel(self, port_handle, access_mask=XLaccess(1), bustype=XL_BUS_TYPE_CAN, flags=XL_ACTIVATE_RESET_CLOCK):
        self.candll.xlActivateChannel.argtypes=[XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        ok=self.candll.xlActivateChannel(port_handle, access_mask, bustype, flags)
        return ok
 
    def close_driver(self):
        ok=self.candll.xlCloseDriver()
        return  ok
 
    def deactivate_channel(self, port_handle=XLporthandle(XL_INVALID_PORTHANDLE), access_mask=XLaccess(1)):
        self.candll.xlDeactivateChannel.argtypes=[XLporthandle, XLaccess]
        ok=self.candll.xlDeactivateChannel(port_handle, access_mask)
        return ok
 
    def close_port(self, port_handle=XLporthandle(XL_INVALID_PORTHANDLE)):
        self.candll.xlClosePort.argtypes=[XLporthandle]
        ok=self.candll.xlClosePort(port_handle)
        return ok
 
    def receive(self, port_handle, event_count, event_list):
        self.candll.xlReceive.argtypes=[XLporthandle, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(XLevent)]
        #ev=XLevent(0)
        #print port_handle, event_count, event_list
        ok=self.candll.xlReceive(port_handle, ctypes.byref(event_count), ctypes.byref(event_list))
        #print event_list
        return ok
 
    def get_event_string(self, ev):
        self.candll.xlGetEventString.argtypes=[ctypes.POINTER(XLevent)]
        self.candll.xlGetEventString.restype=ctypes.c_char_p
        rec_string=self.candll.xlGetEventString(ctypes.pointer(ev))
        return rec_string
 
    def can_set_channel_bitrate(self, port_handle, amask, bitrate):
        self.candll.xlCanSetChannelBitrate.argtypes=[XLporthandle, XLaccess, ctypes.c_ulong]
        ok= self.candll.xlCanSetChannelBitrate(port_handle, amask, ctypes.c_ulong(bitrate))
        return ok
 
    def can_transmit(self, port_handle, amask, message_count, p_messages):
        self.candll.xlCanTransmit.argtypes=[XLporthandle, XLaccess, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p]
        ok=self.candll.xlCanTransmit(port_handle, amask, ctypes.byref(message_count), ctypes.byref(p_messages))
        return ok
 
    def get_error_string(self, err):
        self.candll.xlGetErrorString.argtypes=[XLstatus]
        self.candll.xlGetErrorString.restype=ctypes.c_char_p
        err_string=self.candll.xlGetErrorString(err)
        return err_string
 
class can_api():
    def __init__(self):
        self.driver=candriver()
 
    def channel_init(self):
        self.driver.open_driver()
        self.mask=self.driver.get_channel_mask()
        ok, self.phandle, self.pmask=self.driver.open_port()
        if not(ok):
            ok=self.driver.activate_channel(self.phandle)
        err_string=self.driver.get_error_string(ok)
        return err_string
 
    def channel_close(self):
        self.driver.deactivate_channel(self.phandle, self.mask)
        self.driver.close_port(self.phandle)
        self.driver.close_driver()
 
    def send_msg(self, data, id):
        event_msg=XLevent(0)
        event_msg.tag=XL_TRANSMIT_MSG
        event_msg.tagData.msg.id=id
        event_msg.tagData.msg.flags=0
        dlc=len(data)
        for n in range(0, dlc):
            event_msg.tagData.msg.data[n]=data[n]
        event_msg.tagData.msg.dlc=dlc
        event_count=ctypes.c_uint(1)
        ok=self.driver.can_transmit(self.phandle, self.mask, event_count, event_msg)
        err_string=self.driver.get_error_string(ok)
        return err_string
 
    def get_msg(self):
        event_count=ctypes.c_uint(1)
        #print phandle, event_count
        event_list=XLevent(0)
        ok=self.driver.receive(self.phandle, event_count, event_list)
        if ok:
            rec_string=self.driver.get_error_string(ok)
        else:
            rec_string=self.driver.get_event_string(event_list)
        return rec_string
