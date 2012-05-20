from fl.gameobject.Player import Player
from fl.globals import UP
from fl.items.RPG import RPG
import pygame
import threading
from fl.gameobject.Player import *
            
class msgHandler(object):
    
    def __init__(self, game, client):
        self.game = game
        self.client = client
        
    
    def addPlayer(self,msg):
        self.game.players.add(Player([],100,100,msg[2], msg[1])) 
    
    def movePlayer(self, currentMessage):
        try:
            for player in self.game.players:
                if self.game.player != player:
                    if player.get_name() == currentMessage[1]: 
                        player.position[0] = float(currentMessage[2])
                        player.position[1] = float(currentMessage[3])
                        player.frameCurrent = int(currentMessage[4])
                        player.set_direction(int(currentMessage[5]))
                        player.set_moving(currentMessage[11])
                        if currentMessage[6] == "False":
                            player.is_firing = False
                        else:
                            player.is_firing = True
                            player.remoteCrosshair = (float(currentMessage[7]), float(currentMessage[8]))
                            player.shootingPosition[0] = float(currentMessage[9])
                            player.shootingPosition[1] = float(currentMessage[10])
        except TypeError:
            self = self
    
    def sendCurrentPos(self):
        x,y = self.game.player.get_position()
        name = self.game.player.get_name()
        skin = self.game.player.get_skin()
        msg = "102+"+str(x)+"+"+str(y)+"+"+skin+"+"+name
        return msg
                    
    def addInGamePlayer(self,msg):
        print "Coordenada um " + msg[1]
        print "Coordenada dois " + msg[2]
        self.game.players.add(Player([],float(msg[1]),float(msg[2]),msg[3],msg[4]))
        
    def killPlayer(self, msg):
        for player in self.game.players:
            if self.game.player != player:
                if player.get_name() == msg[1]:
                    player.position[0] = -1
                    player.position[1] = -1
                    player.update_position()
                    player.dead = True
                    if self.game.player.name == msg[2]:
                        self.game.player.playKilled = self.game.player.playKilled + 1
   
    def deleteItem(self, msg):
        for item in self.game.items:
            if item.position[0] == int(msg[2]) and item.position[1] == int(msg[3]):
                item.toDelete = True
        #if weapon pickup
        for player in self.game.players:
            if self.game.player != player:
                if player.get_name() == msg[1]:
                    if msg[4] == "RPG":
                        player.pickup(RPG())
                    elif msg[4] == "LaserRifle":
                        player.pickup(LaserRifle())         
 
    def relocatePlayer(self,msg):
        for player in self.game.players:
            if self.game.player != player:
                if player.get_name() == msg[1]:
                    player.position[0] = 100
                    player.position[1] = 100
                    player.update_position()
                    player.dead = False
                    
                    