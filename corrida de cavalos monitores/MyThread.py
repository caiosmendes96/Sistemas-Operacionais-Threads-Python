class MyThread():
    
    def __init__(self, posX, posY, idThread, actionsTest):
        self.posX = posX
        self.posY = posY
        self.idThread = idThread
        self.score = 0
        self.actions = ['right', 'up', 'down']
        self.finished = False
        self.actionsTest = actionsTest
        self.waitTimer = None 
        self.totalWaitTimer = 0
        
    def getWaitTimer(self):
        return self.waitTimer
    
    def setWaitTimer(self, time):
        self.waitTimer = time

    def getTotalWaitTimer(self):
        return self.totalWaitTimer
    
    def setTotalWaitTimer(self, time):
        self.totalWaitTimer = time
    def getExecutor(self):
        return self.executor
    
    def getPosX(self):
        return self.posX
    
    def getPosY(self):
        return self.posY
    
    def setPosX(self, posX):
        self.posX = posX
        
    def setPosY(self, posY):
        self.posY = posY
        
    def getScore(self):
        return self.score
    
    def setScore(self,score):
        self.score = score
         
    def getIdThread(self):
        return self.idThread  
     
    def addScore(self,score):
        self.score += score
                
    def checkIfFinished(self):
        if self.getPosY() >= 4:
            self.finished = True
            return True
        return False
    