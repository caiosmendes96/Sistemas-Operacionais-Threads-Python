import threading
import time
class Monitor():
    
    def __init__(self):
        
        self.lock = threading.Lock()
        self.waitCount = 0
        
    def startTimer(self, thread):
        if thread.getWaitTimer() is None:
                thread.setWaitTimer(time.time())
                #print("Iniciou timer \n")
                
    def stopTimer(self,thread):
        if thread.getWaitTimer() is not None:
            wait_time = time.time() - thread.getWaitTimer()
            thread.totalWaitTimer += wait_time
            thread.setWaitTimer(None)   

    def acquire(self, thread):
        
        acquired = self.lock.acquire(timeout=0.2)
        if acquired:
            print(f"Thread {thread.getIdThread()} adquiriu o mapa_lock. \n")
            self.stopTimer(thread)
        else:
            self.startTimer(thread)
            print(f"Thread {thread.getIdThread()} precisou aguardar para adquirir o mapa_lock. \n")
            self.waitCount += 1
        
        return acquired
            
    def release(self, thread):
        self.lock.release()
    
    def getWaitCount(self):
        with self.lock:
            return self.waitCount 
        
        