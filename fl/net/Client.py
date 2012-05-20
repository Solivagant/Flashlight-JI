'''
Created on Nov 24, 2009

@author: phillopes
'''
import socket
import sys
import threading
from fl.base.Game import Game
from fl.net.Network import *

class Client(object):
    #"192.168.1.101"
    def __init__(self, name, game, host="localhost", port=8740):
        
        self.name = name
        self.game = game
        self.host = host
        self.port = port
        
        try:
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
        except socket.error, e:
            print "Could not connect to the server ! "
            print e
            sys.exit(1)

        print "The Client has connected to the server, and is ready to communicate !"
        
        #Creating the Message Handler
        self.game.msgHandler = msgHandler(self.game, self)
        
        #Start Receiving Thread
        self.receiver = waitanswer(self.socket, self.game.msgHandler, self)
        self.receiver.start()
        
        self.treatOutgoing("100+"+self.game.player.name+"+"+self.game.player.skin+"+pos")
        
    def treatOutgoing(self, msg):

        if len(msg):
        
            if msg == "E" or msg == "e":
                # Tells the thread to stop and checks the flag of the thread before closing socket
                self.receiver.stop()
                while 1:
                    if self.receiver.stopped() :
                        self.socket.close()
                        sys.exit(1)
                        
            else:
                self.socket.send(msg)
    
    def killClient(self):
        self.receiver.stop()
        while 1:
            if self.receiver.stopped() :
                self.socket.close()
    
#Thread that will wait for server responses
class waitanswer(threading.Thread):
    
    def __init__(self, socket, msgHandler, client):
        self.socket = socket
        self.msgHandler = msgHandler
        self.client = client
        self._stop = threading.Event()
        threading.Thread.__init__(self)
        
    def run (self):
        
        while 1:
            
            data = self.socket.recv(1024)
            
            if len(data):
                
                #print "Olha aqui o data" + data
                
                parser = data.split('+')
                
                if parser[0] == "101":
                    self.msgHandler.addPlayer(parser)
                    msg = self.msgHandler.sendCurrentPos()
                    self.client.treatOutgoing(msg)
                
                if parser[0] == "102":
                    print "recebi addinGame player"
                    self.msgHandler.addInGamePlayer(parser)
                    
                if parser[0] == "200":
                    self.msgHandler.movePlayer(parser)
                    
                if parser[0] == "105":
                    self.msgHandler.killPlayer(parser)
                
                if parser[0] == "301":
                    self.msgHandler.deleteItem(parser)
                
                if parser[0] == "161":
                    self.msgHandler.relocatePlayer(parser)
    
    # Raises a flag stating that the thread has stopped
    def stop(self):
        self._stop.set()
    
    # Returns the stoppage flag
    def stopped (self):
        return self._stop.isSet()
    
    def getData(self):
        return self.data
    

    
            
            


            