from fl.audio.AudioResource import AudioResource
from fl.gameobject.GameObject import GameObject
from fl.gameobject.Player import Player
from fl.globals import * #@UnusedWildImport
from fl.items import Weapon, Rifle, LaserRifle
from fl.items.Rifle import *
from fl.items.LaserRifle import *
from fl.gameobject.Player import *
from fl.ai.FSM import *
from fl.ai.State import *
from random import random
import random

class Enemy(Player):

    # Constructor
    def __init__(self, array, x, y, filename, name, stateMachine=None):
        Player.__init__(self, array, x, y, filename, name)
        self.stateMachine = stateMachine
        self.setRandomDirection()
        self.hasGround = True
        self.frameCurrent = 1
        self.hitWall = False
        
    def setRandomDirection(self):
        if random.random() > 0.5:
            self.direction = RIGHT
        else:
            self.direction = LEFT        
        
    def update(self):
        #

        if self.stateMachine != None:
            if self.hitWall == True:
                self.stateMachine.nextState((0,1,0)) 
            else:  
                self.stateMachine.nextState((0,0,0))        
            currentState = self.stateMachine.getCurrentState()
    
            if isinstance(currentState, StateMoveCurrentDirection):
                self.moveX = 0
                self.moveY = 0 
                if self.direction == LEFT:
                    self.next_frame()
                    self.isMoving = True
                    self.movement = (WALK_SPEED, 0, LEFT)
                    if random.random() > 0.9:
                        self.is_firing = True
                    else:
                        self.is_firing = False                     
                elif self.direction == RIGHT:
                    self.next_frame()
                    self.isMoving = True
                    self.movement = (WALK_SPEED, 0, RIGHT)
                    if random.random() > 0.9:
                        self.is_firing = True
                    else:
                        self.is_firing = False                     
    
            elif isinstance(currentState, StateChangeDirection):
                self.hitWall = False
                self.isMoving = False
                self.set_reverse_direction()          
            

        