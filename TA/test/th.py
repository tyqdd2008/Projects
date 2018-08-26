import threading
import time

class Mythread(threading.Thread):

    def __init__(self, arg):
        super(Mythread, self).__init__()
        self.arg = arg

    def run(self):
        time.sleep(1)
        print(self.arg)

if __name__ == "__main__":
    
    for i in range(4):
        th = Mythread(i)
        th.start()
    
        
        
        
