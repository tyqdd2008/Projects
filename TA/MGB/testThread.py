import threading
import time
import ctypes
import inspect
import traceback,sys

'''
class test1(object):
    #############################
    def __init__(self):
        pass
    
    #############################
    #This fun perform threading function which is
    #get from another class
    def threadFun(self):
        print "This is a test threading!"
        tarClass = test2()
        self.thTest = threading.Thread(target=tarClass.tesTarget,args=("Masion",))
        watchThread = watchDog(1,self.thTest)
        self.thTest.start()
        self.stop()
        self.thTest.join()
        
        print "Now thread is over"
    ################################
    #Stop thread
    def stop(self):
        watchThread = watchDog(1,self.thTest)
        watchThread.start()
'''
#####################################

class test1(threading.Thread):
    ##################
    def __init__(self):
        threading.Thread.__init__(self)

    ##################
    def run(self):
       time.sleep(3)
       for i in range(10):
           print "Test1 thread is over"
           time.sleep(1)
          

############################################
#Another class for test
class test2(object):
    #######################
    def __init__(self):
        pass

    ########################
    def tesTarget(self,name):
        print "Test name is", name
        #time.sleep(10)
        while(1):
            print "Not over"

############################################
#WatchDog Class
class watchDog(threading.Thread):
    ##################
    def __init__(self,timeout,thread):
        threading.Thread.__init__(self)
        self.thread = thread
        self.timeout = timeout

    ##################
    def run(self):
        self.stop_thread()
        print "WatchDog is over"
        
    ##################
    #Stop thread
    def stop_thread(self):
        tid = ctypes.c_long(self.thread.ident)
        print "tid", tid
        time.sleep(self.timeout)
        exctype = ctypes.py_object(SystemExit)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            print res
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")     

#############################################
if __name__ == "__main__":
    try:
        result = test1()
    except:
        traceback.print_exc(file = sys.stdout)
    result.start()
    #result.threadFun()
    try:
        watchThread = watchDog(1,result)
    except:
        traceback.print_exc(file=sys.stdout)
    watchThread.start()
    watchThread.join()
    #result.join()    
    print "Main process is over!"
        
