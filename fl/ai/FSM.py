'''
Created on 2009/12/14
Finite State Machine - Maquina de Estados Finita
Serve para guiar os inimigos nas varias accoes que podem realizar
@author: Solivagant
'''
from State import *

class SimpleFSM(object):

    '''
    Constructor
    '''
    def __init__(self):
        self.states = []
        self.states.append(StateHalt()) #estado S0
        self.states.append(StateMoveCurrentDirection()) #estado S1
        self.states.append(StateChangeDirection()) #estado S2        
        self.states.append(StateMoveTowards()) #estado S3
        self.states.append(StateFire()) #estado S4
        self.states.append(StateDie()) #estado S5
        self.startState = 0
        self.currentState = self.startState
        self.finalState = 5
           
    def getCurrentState(self):
        return self.states[self.currentState]
    
    def nextState(self, (sawPlayer, hitWall, nearPlayer)):
        if self.currentState == 0:
            if sawPlayer:
                self.currentState = 3
            else:
                self.currentState = 1
        elif self.currentState == 1:
            if hitWall:
                self.currentState = 2
        elif self.currentState == 2:
            self.currentState = 0
        elif self.currentState == 3:
            if sawPlayer and nearPlayer:
                self.currentState = 4
        elif self.currentState == 4:
            if sawPlayer and not nearPlayer:
                self.currentState = 3
            else:
                self.currentState = 1
                
        return self.getCurrentState()    
        
        