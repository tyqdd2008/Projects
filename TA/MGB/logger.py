#!coding=utf-8
import logging
import os
import time

LEVELS={'debug':logging.DEBUG,\
        'info':logging.INFO,\
        'warning':logging.WARNING,\
        'error':logging.ERROR,\
        'critical':logging.CRITICAL,}
         
logger=logging.getLogger()
level='default'
def createFile(filename):
    path=filename[0:filename.rfind('\\')]                           
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        #Create a new file
        fd = open(filename,mode='w')
        fd.close()
class MyLog:
    log_filename=r'D:\Temp\TA\Log\itest.log'
    err_filename=r'D:\Temp\TA\Log\err.log'
    dateformat='%Y-%m-%d %H:%M:%S'
    logger.setLevel(LEVELS.get(level,logging.NOTSET))
    createFile(log_filename)
    createFile(err_filename)

    handler=logging.FileHandler(log_filename,encoding='utf-8')
    errhandler=logging.FileHandler(err_filename,encoding='utf-8')

    @staticmethod    
    def debug(log_message):
        setHandler('debug')
        logger.debug("[DEBUG "+getCurrentTime()+"]"+log_message)
        removerhandler('debug')

    @staticmethod
    def info(log_message):
        setHandler('info')
        logger.info("[INFO "+getCurrentTime()+"]"+log_message)
        removerhandler('info')
     
    @staticmethod
    def warning(log_message):
        setHandler('warning')
        logger.warning("[WARNING "+getCurrentTime()+"]"+log_message)
        removerhandler('warning')

    @staticmethod
    def error(log_message):
        setHandler('error')
        logger.error("[ERROR "+getCurrentTime()+"]"+log_message)
        removerhandler('error')

    @staticmethod
    def critical(log_message):
        setHandler('critical')
        logger.critical("[CRITICAL "+getCurrentTime()+"]"+log_message)
        removerhandler('critical')



def setHandler(level):
    if level=='error':
        logger.addHandler(MyLog.errhandler)

    logger.addHandler(MyLog.handler)

def removerhandler(level):
    if level=='error':
        logger.removeHandler(MyLog.errhandler)
    logger.removeHandler(MyLog.handler)

def getCurrentTime():
    return time.strftime(MyLog.dateformat,time.localtime(time.time()))

if __name__=="__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error message")
    MyLog.critical("This is critical message")
