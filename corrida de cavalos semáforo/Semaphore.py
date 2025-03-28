import threading
import time
class Semaphore():
    def __init__(self, initial):
        self.count = initial
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.waitCount = 0
        self.printLock = threading.Lock()
        
    def startTimer(self, thread):
        if thread.getWaitTimer() is None:
                self.waitCount += 1
                thread.setWaitTimer(time.time())
                
    def stopTimer(self,thread):
        
        if thread.getWaitTimer() is not None:
            wait_time = time.time() - thread.getWaitTimer()
            thread.totalWaitTimer += wait_time
            thread.setWaitTimer(None)        
                    
    def acquire(self, thread, printLock):
        
        with self.condition:
            while self.count == 0:
                self.startTimer(thread)
                self.waiting = True
                with printLock:
                    print(f"Thread {thread.idThread} precisou aguardar para adquirir o mapa_lock. \n")
                self.condition.wait()
                
            self.count -= 1
            

    def getWaitCount(self):
        with self.lock:
            return self.waitCount    
            
    def release(self,thread):
        
        with self.condition:
            self.stopTimer(thread)
            self.count += 1
            #print(f"Thread {thread.idThread} acaba de liberar o Lock. \n")
            self.condition.notify()