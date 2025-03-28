import time
import threading
from Semaphore import Semaphore
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
        
        self.trackLocks = [[Semaphore(1) for _ in range(self.columns)] for _ in range(self.rows)]  #Matriz de semáforos
            
        self.actions = [ #Ações pre definidas
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
            ["right","right","down","right","right"],
            ["down","right","right","right","down","right"],
            ["up","right","right","right","right"],
        ]
        self.placing = []
        self.placing_lock = threading.Lock()
        self.printLock = threading.Lock()
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
        return (0 <= posX < self.rows and 0 <= posY < self.columns)

    def addThread(self, thread):
        self.threads.append(thread)
    
    def changeScoreTrack(self, posX, posY):
        if self.positionIsValid(posX, posY):
            self.trackPoints[posX][posY] -= 1
                
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
        
    def changeScorePlacement(self,thread):
        thread.addScore(self.scorePlacement)
        self.scorePlacement -= 3
        
    def printAllWaitCounter(self):
        counter = 0
        for row in self.trackLocks:
            for semaphore in row:
                counter += semaphore.getWaitCount()   
        print("Quantidade de ocorrência (condicao de corrida): ", counter, "\n")     
        
    def printAllTotalWaitTimer(self):
        for thread in self.threads:  
            print("Tempo de espera para a thread", thread.getIdThread(),": ", thread.getTotalWaitTimer(), "\n")     
            
    ######## FUNÇÃO PRINCIPAL ############       
        
    def moveThread(self, thread): #Função "main" de cada thread que gerencia a movimentação, pontuação e solução para condição de corrida
        index = 0
        while index < len(thread.actionsTest): #Loop de execução para cada ação pré definida das threads
            
            action = thread.actionsTest[index]  #Pega a ação da vez
            newPosX, newPosY = thread.posX, thread.posY

            if action == "right" and thread.posY < 4: #Define a posição futura a partir da ação
                newPosY += 1
            elif action == "up" and thread.posX > 0:
                newPosX -= 1
            elif action == "down" and thread.posX < 10:
                newPosX += 1
                
            with self.printLock:
                print(f"Thread {thread.idThread} ação requerida: {action}\n")           
                                                               #Matriz de Semáforos com tamanho igual a matriz Track para garantir a consistencia da pontuação a cada movimentação
            self.trackLocks[newPosX][newPosY].acquire(thread, self.printLock)   #Cada thread tenta garantir a região crítica para a posição futura calculada na matriz trackLocks 
            print(f"Thread {thread.getIdThread()} adquiriu o mapa_lock. \n")
            time.sleep(0.5) 

            if self.positionIsValid(newPosX, newPosY) and thread.finished != True: #Com a região crítica liberada, é checado se a movimentação futura é válida
                with self.printLock:
                    print(f"Thread {thread.idThread} ação realizada: {action}\n")
                    self.updateTrack(newPosX,newPosY,thread) #Atualiza a posição do cavalo na Track
                    thread.setPosX(newPosX) #Atualiza a sua posição
                    thread.setPosY(newPosY)
                    thread.addScore(self.trackPoints[newPosX][newPosY]) #Adiciona a pontuação referente a sua movimentação na Track/trackPoints
                    self.changeScoreTrack(newPosX, newPosY) #Diminui 1 ponto na posição da Track em que o cavalo se movimentou
                    self.printTrack() #Mostrar a Track atualizada após a movimentação
                    
                index += 1  #Vai para a próxima ação pré definido

            
            if thread.checkIfFinished(): #Checa se o cavalo chegou a linha final
                self.placing.append(thread.getIdThread()) #Se chegou, adiciona o cavalo na lista de colocação em ordem de chegada
                self.changeScorePlacement(thread)  #Diminui 3 pontos para o próximo cavalo que chegar no final
            self.trackLocks[newPosX][newPosY].release(thread) #Libera essa posição da trackLock para as threads 
