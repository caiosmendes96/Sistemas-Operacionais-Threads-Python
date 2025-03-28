import time
import threading
from colorama import init, Fore, Style

init()

class Track:
    def __init__(self):
        self.rows = 11
        self.columns = 5
        self.threads = []
        self.track = [
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []],
            [[], [], [], [], []]
        ]
        self.trackPoints = [
            [2, 2, 2, 2, 9],
            [0, 2, 2, 2, 9],
            [2, 2, 2, 2, 9],
            [0, 2, 2, 2, 9],
            [2, 2, 2, 2, 9],
            [0, 2, 2, 2, 9],
            [2, 2, 2, 2, 9],
            [0, 2, 2, 2, 9],
            [2, 2, 2, 2, 9],
            [0, 2, 2, 2, 9],
            [2, 2, 2, 2, 9]
        ]
        
        self.trackLocks = [[threading.Lock() for _ in range(self.columns)] for _ in range(self.rows)]    
            
        self.actions = [
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
            ["right","right","down","right","right"],
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
        ]
        self.placing = []
        self.printLock = threading.Lock()
        self.updateLock = threading.Lock()
        self.scorePlacement = 15
        self.waitCount = 0
        
        
    def getTrack(self):
        return self.track
    
    def getActions(self):
        return self.actions
    
    def getThreads(self):
        return self.threads
    
    def getWaitCount(self):
        return self.waitCount
    
    def positionIsValid(self, posX, posY):
        return 0 <= posX < self.rows and 0 <= posY < self.columns

    def addThread(self, thread):
        self.threads.append(thread)
    
    def printAllScores(self):
        for thread in self.threads:
            print("Thread id:", thread.idThread, "| Score:", thread.getScore())
    
    def updateTrack(self, newPosX, newPosY, thread): 
          
        self.track[thread.posX][thread.posY].remove(thread.getIdThread())
        self.track[newPosX][newPosY].append(thread.getIdThread())
        
    def printTrack(self):
        color_map = {
            1: Fore.RED,
            2: Fore.GREEN,
            3: Fore.BLUE,
            4: Fore.YELLOW,
            5: Fore.CYAN,
            '-': Fore.WHITE
        }
        print("\n")  
        for row in self.track:
            for cell in row:
                if cell:  # Se houver threads na célula
                    colors = [color_map.get(int(thread_id), Fore.WHITE) + str(thread_id) for thread_id in cell]
                    print("[" + ", ".join(colors) + "]", end=' ')
                else:
                    print(Fore.WHITE + "[ ]", end=' ')
            print()
        print("\n")    
        
    def printTrackPoints(self):
        for row in self.trackPoints:
            print('\t'.join(map(str, row)))    
    
    def printPlacing(self):
        print(" - Ordem de chegada dos cavalos - \n")
        print("1º  2º  3º  4º  5º \n")
        print(self.placing, "\n")  
        
    def changeScoreTrack(self, posX, posY):
        if self.positionIsValid(posX, posY):
            self.trackPoints[posX][posY] -= 1
                
    def changeScorePlacement(self,thread):
        thread.addScore(self.scorePlacement)
        self.scorePlacement -= 3
    
    def printAllWaitCount(self):
        print("Quantidade de ocorrência (condição de corrida): ", self.getWaitCount(), "\n")     
        
    def printAllTotalWaitTimer(self):
        for thread in self.threads:  
            print("Tempo de espera para a thread", thread.getIdThread(),": " , thread.getTotalWaitTimer(), "\n")     
            
    def startTimer(self, thread):
        if thread.getWaitTimer() is None:
                thread.setWaitTimer(time.time())
                #print("Iniciou timer \n")
                
    def stopTimer(self,thread):
        
        if thread.getWaitTimer() is not None:
            wait_time = time.time() - thread.getWaitTimer()
            thread.totalWaitTimer += wait_time
            thread.setWaitTimer(None)        
                    
           
    def moveThread(self, thread):

        index = 0
        while index < len(thread.actionsTest):
            
            action = thread.actionsTest[index]
            newPosX, newPosY = thread.posX, thread.posY
            
            if action == "right" and thread.posY < 4:
                newPosY += 1
            elif action == "up" and thread.posX > 0:
                newPosX -= 1
            elif action == "down" and thread.posX < 10:
                newPosX += 1
                
            with self.printLock:
                print(f"Thread {thread.idThread} ação requerida: {action}\n")     
                      
            if self.trackLocks[newPosX][newPosY].acquire(timeout = 0.2):
                try:
                    print(f"Thread {thread.getIdThread()} adquiriu o mapa_lock. \n")
                    self.stopTimer(thread)
                    time.sleep(0.5)

                    if self.positionIsValid(newPosX, newPosY) and thread.finished != True:
                        
                        with self.printLock:
                            print(f"Thread {thread.idThread} ação realizada: {action}\n")                
                            self.updateTrack(newPosX,newPosY,thread)
                            thread.setPosX(newPosX)
                            thread.setPosY(newPosY)
                            thread.addScore(self.trackPoints[newPosX][newPosY]) 
                            self.changeScoreTrack(newPosX, newPosY)  
                            self.printTrack()     
                            
                    if thread.checkIfFinished():
                        self.placing.append(thread.getIdThread())
                        self.changeScorePlacement(thread)  
                        
                finally:
                    
                    self.trackLocks[newPosX][newPosY].release()
                    print(f"Thread {thread.idThread} acaba de liberar o Lock. \n")
                index += 1   
            else:
                self.startTimer(thread)
                
                with self.printLock:
                    self.waitCount += 1
                print(f"Thread {thread.idThread} precisou aguardar para adquirir o mapa_lock. \n")
            
            
            
