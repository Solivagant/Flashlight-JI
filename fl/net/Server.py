from Msg import MsgConnect, MsgNewPlayer, MsgScoreUpdate
from asyncore import *
import threading
import socket
import sys

# Nota ainda e necessario de tratar dos varios protocolos aqui do servidor
# dependendo das varias respostas do cliente. Secalhar deveriamos pensar em
# criar uma funcao onde mandariamos a string recebida e esta trataria em transforma-la
# num objecto, onde seria mais facil ser lida pelo jogo. Nota que isto pode ser mau
# em termos de optimizacoes !!


class Server(threading.Thread):
    
    port = 8740
    buffer = 1024
    
    listplayers = [] # Lista de jogadores que estao correntemente a jogar!
                     
    maplist = "TempMap" # Definida pelo administrador do servidor !!!
    
    maxKill = 0 # Definida tambem pelo administrador do servidor! Death Cap
    

    #Funcao de inicializacao do Servidor
    def __init__ (self):
        
        #Inicializacao do servidor
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', self.port))
            self.socket.listen(3)
            threading.Thread.__init__(self)
        except socket.error, e:
            print " Couldn't Create Socket ! for error ", e
            sys.exit(1)
        
    # Main Loop
    def run(self):
        
        print " The Server is Currently Running!! "
        
        inputs = [self.socket]
        outputs = []
        
        running = 1
        
        self.latestPlayer = None
        
        ## Server is Active Awaiting Input !! 
        while running:
            
            try:
                inputready, outputready, exceptready = select.select(inputs, outputs, inputs)
            except select.error, e:
                break
            except socket.error, e:
                break


            for s in inputready:
                 
                if s == self.socket:
                    
                    client, address = self.socket.accept()
                    print " A new client has connected his address is - ", client.getpeername()
                    
                    # Inserting clients to the input bound and output bound socket family
                    inputs.append(client)
                    outputs.append(client)
                    
                    
                else:
                    
                    # Receive Data from the Socket and process it !
                    try:
                        
                        data = s.recv(self.buffer)
                        if not len(data):
                            print " Connection to host ", s.getpeername(), " has been lost!"
                            inputs.remove(s)
                            outputs.remove(s)
                            s.close()
                            
                        else:
                            parser = data.split('+')
                            if parser[0] == "100":
                                print "I received this message code 100 from peer ", s.getpeername()
                                self.newPlayer(parser[1])
                                sender = MsgNewPlayer(parser[1], parser[2], parser[3])
                                self.latestPlayer = s
                                for out in outputready:
                                    if s is not out:
                                        out.send(sender.toString())
                            
                            
                            elif parser[0] == "102":
                                print "I received this message code 102 from peer ", s.getpeername()
                                for out in outputready:
                                    if s is not out and s is not self.latestPlayer:
                                        out.send(data)
                                    
                            
                            #Gamestate updater, this functions objective is to relay
                            #the DEAD player information from a player X and send it to all other
                            #players in the game.
                            elif parser[0] == "105":
                                #print "I received this message code 105 from peer ", s.getpeername()
                                for out in outputready:
                                    if s is not out:
                                        out.send(data)
    
                            #Gamestate updater, this functions objective is to relay
                            #the ACTION information from a player X and send it to all other
                            #players in the game.
                            elif parser[0] == "110":
                                #print "I received this message code 110 from peer ", s.getpeername()
                                self.newPlayer(parser[1])
                                sender = MsgNewPlayer(parser[1], parser[2], parser[3])
                                for out in outputready:
                                    if s is not out:
                                        out.send(sender.toString())
                            
                            #Gamestate updater, this functions objective is to relay
                            #the FIRE information from a player X and send it to all other
                            #players in the game.
                            elif parser[0] == "112":
                                #print "I received this message code 112 from peer ", s.getpeername()
                                self.newPlayer(parser[1])
                                sender = MsgNewPlayer(parser[1], parser[2], parser[3])
                                for out in outputready:
                                    if s is not out:
                                        out.send(sender.toString())
                                                    
                            #Gamestate updater, this functions objective is to relay
                            #the updated information from a player X and send it to all other
                            #players in the game.
                            elif parser[0] == "200":
                                #print "I received this message code 200 from peer ", s.getpeername()
                                for out in outputready:
                                    if s is not out:
                                        out.send(data)
                            
                            #Scoreboard updater, sends to the client the updated information
                            #about score and the time.
                            elif parser[0] == "201":
                                #print "I received this message code 201 from peer ", s.getpeername()
                                sender = MsgScoreUpdate(parser[1], parser[2], parser[3])
                                for out in outputready:
                                    out.send(sender)
                            
                            #ITEM PICKUP       
                            elif parser[0] == "301":
                                #print "I received this message code 301 from peer ", s.getpeername()
                                for out in outputready:
                                    out.send(data)
                                                                        
                            else:
                                print "Invalid Msg Code or Doesn't Exist !!" 
                                print "Message Code Received --> ", parser[0]
                                print "Full Extent of the Message --->" , data         
                    except socket.error, e:
                        print "Connection Reset by peer"
                        inputs.remove(s)
                        outputs.remove(s)
                        s.close() 
            
    # The Client must send a msg with this structure -
    # msgcode+playername+avatar+respawnpoint
            
    def newPlayer(self, name):
        self.id = len(self.listplayers) + 1
        self.listplayers.append((id, name, 0)) # The tuple is player id, player name and respective score
    
    # Packs all the player scores into a list
    def getScore(self, players):
        scores = []
        for player in players:
            scores.append(player[3])
        return scores
    
    #Checks if any of the scores in the list has reached or surpassed the Score Cap
    def maxScore(self, scores):
        for s in scores:
            if s >= self.scoreCap:
                return True
        return False
