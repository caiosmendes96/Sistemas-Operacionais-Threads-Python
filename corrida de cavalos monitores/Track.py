import time
import random
import threading
from Monitor import Monitor
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
        
        self.trackLocks = [[Monitor() for _ in range(self.columns)] for _ in range(self.rows)]    
            
        self.actions = [
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
            ["right","right","down","right","right"],
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
        ]
        self.placing = []
        self.print_lock = threading.Lock()
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

    def changeScoreTrack(self, posX, posY):
        if self.positionIsValid(posX, posY):
            self.trackPoints[posX][posY] -= 1
    
    def positionIsValid(self, posX, posY):
        return 0 <= posX < self.rows and 0 <= posY < self.columns

    def addThread(self, thread):
        self.threads.append(thread)
    
    def printAllScores(self):
        for thread in self.threads:
            print("Thread id:", thread.idThread, "| Score:", thread.getScore())
            
    def printAllWaitCount(self):
            print("contador de quantas vezes ocorreu condicao de corrida: ", self.getWaitCount(), "\n")    
             
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
                if cell:  
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
        
    def changeScorePlacement(self,thread):
        thread.addScore(self.scorePlacement)
        self.scorePlacement -= 3 
    
    def printAllWaitCounter(self):
        counter = 0
        for row in self.trackLocks:
            for monitor in row:
                counter += monitor.getWaitCount()   
        print("Quantidade de ocorrência (condicao de corrida): ", counter, "\n") 
        
    def printAllTotalWaitTimer(self):
        for thread in self.threads:  
            print("Tempo de espera para a thread", thread.getIdThread(),": ", thread.getTotalWaitTimer(), "\n")     
                               
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
            print(f"Thread {thread.idThread} ação requerida: {action}\n")           
            
            if self.trackLocks[newPosX][newPosY].acquire(thread):
                try: 
                    time.sleep(0.5) 
                        
                    if self.positionIsValid(newPosX, newPosY) and thread.finished != True:
                        with self.print_lock:
                            print(f"Thread {thread.getIdThread()} ação realizada: {action}\n")           
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
                    self.trackLocks[newPosX][newPosY].release(thread)
                    index += 1  
            
