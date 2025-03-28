from Track import Track
from MyThread import MyThread
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, Style, init
init()

class Game:
    def __init__(self):
        self.track = Track()
        self.player1 = {
            'bank': 0,
            'bet': None,
            'predict': None
        }
        self.player2 = {
            'bank': 0,
            'bet': None,
            'predict': None
        }

    def createThreads(self): #Criação das threads e posicionando-os na Track (posições posX: 1, 3, 5, 7, 9)
        for i in range(1, 6):
            posX = 2 * i - 1
            posY = 0
            if posX < self.track.rows:
                thread = MyThread(posX, posY, i, self.track.actions[(i-1)])
                self.track.track[posX][posY].append(i)
                self.track.addThread(thread)

    def startThreads(self): #Início das threads 
        with ThreadPoolExecutor(max_workers=5) as executor:         
            executor.submit(self.moveThreads,0)
            executor.submit(self.moveThreads,1)
            executor.submit(self.moveThreads,2)
            executor.submit(self.moveThreads,3)
            executor.submit(self.moveThreads,4)
              
    def moveThreads(self, i): 
        thread = self.track.threads[i]
        self.track.moveThread(thread)

    def checkWinner(self):
        
        winnerThread = max(self.track.getThreads(), key=lambda item: item.score)
        print("Cavalo ganhador: ", winnerThread.getIdThread())
        
        return winnerThread.getIdThread()
    
    def checkBet(self):
        if self.player1['predict'] == self.checkWinner():
            self.player1['bank'] += self.player2['bet']
            self.player1['bank'] += self.player1['bet']
            print("Player 1 ganhou! \n")
        elif self.player2['predict'] == self.checkWinner():
            self.player2['bank'] += self.player2['bet']
            self.player2['bank'] += self.player1['bet']
            print("Player 2 ganhou! \n")
        else:
            print("Parabéns! Vocês perderam! \n")
            
    def printBankPlayers(self):
        print(Fore.RED + 'Bank Player 1: ', self.player1['bank'], '\n' + Style.RESET_ALL)
        print(Fore.BLUE + 'Bank Player 2: ', self.player2['bank'], '\n' + Style.RESET_ALL)
        
    def changeBankPlayers(self):
            self.player1['bank'] -= self.player1['bet']
            self.player2['bank'] -= self.player2['bet']
        
    def gameInitialization(self): #Parte inicial dos jogos para captura das informações e apostas
        
        print(Back.GREEN + "Bem vindo a corridona! \n" + Style.RESET_ALL)
        
        print(Back.RED + "Player 1 \n" + Style.RESET_ALL)
        
        self.player1['bank'] = int(input("Digite o valor R$ da sua banca: \n"))
        
        print(Back.BLUE + "Player 2 \n" + Style.RESET_ALL)
        
        self.player2['bank'] = int(input("Digite o valor R$ da sua banca: \n"))
        
        print(Back.MAGENTA + "LISTA DE CAVALOS: \n" + Style.RESET_ALL)
        print(Fore.RED +   "Cavalo 1: Vermelho \n " + Style.RESET_ALL)
        print(Fore.GREEN +  "Cavalo 2: Verde \n " + Style.RESET_ALL)
        print(Fore.BLUE +   "Cavalo 3: Azivis \n " + Style.RESET_ALL)
        print(Fore.YELLOW + "Cavalo 4: Amarelo \n " + Style.RESET_ALL)
        print(Fore.CYAN +  "Cavalo 5: Ciano \n " + Style.RESET_ALL)
        
        print(Back.RED + "Player 1 \n" + Style.RESET_ALL)
        
        self.player1['predict'] = int(input("Digite o numero do cavalo que você irá apostar: "))
        self.player1['bet'] = int(input("Digite o valor R$ da sua aposta: "))

        
        print(Back.BLUE + "Player 2 \n" + Style.RESET_ALL)
        
        self.player2['predict'] = int(input("Digite o numero do cavalo que você irá apostar: "))
        self.player2['bet'] = int(input("Digite o valor R$ da sua aposta: "))
        
        self.changeBankPlayers()
        
    def checkFinish(self):
        if all(thread.finished for thread in self.track.threads):
            return True
        return False
        

game = Game()
game.gameInitialization() #Parte inicial dos jogos para captura das informações e apostas

game.createThreads()
game.track.printTrack()
game.startThreads()

if(game.checkFinish()): #Checa a corrida acabou (todos os cavalos chegaram no final)
    game.checkBet() #Checa e mostra se houve ganhador da aposta
    game.printBankPlayers() #Mostra o banco final dos jogadores
   
game.track.printPlacing() #Mostra a ordem de chegada dos cavalos
game.track.printAllScores() #Mostra a pontuação de cada cavalo
game.track.printAllWaitCounter() #Mostra a quantidade de condições de corrida que ocorreram
game.track.printAllTotalWaitTimer() #Mostra o tempo em que cada thread ficou esperando para adquirir a região critica
