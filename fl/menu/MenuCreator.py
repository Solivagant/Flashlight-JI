# -*- coding: utf-8 -*-
import pygame

#DEFINI�AO CORES

## RGB color for Black
BLACK = (0, 0, 0)

## RGB color for White
WHITE = (255, 255, 255)

## RGB color for Red
RED = (255, 0, 0)

## RGB color for Green
GREEN = (0, 255, 0)

## RGB color for Blue
BLUE = (0, 0, 255)

class cMenu(object):

    def __init__(self, menu_options,background, bckg):

        self.background = background
        self.menu_options = menu_options
        self.bckg = bckg.copy()      

        self.renderedObjects = []

        self.setfont()
        self.updateMenu(0)

    def setfont(self):
        self.font = pygame.font.Font(None, 32)
        self.fontchosen = pygame.font.Font(None, 40)

    def drawMenu(self):
        spaceinc = 0
        self.background.blit(self.bckg, (0,0))
        for x in self.renderedObjects:
            self.background.blit(x,( (self.background.get_width() / 2) - (x.get_width() / 2), (self.background.get_height() / 3) + spaceinc ) )
            spaceinc += 40

    def updateMenu(self, state):

        del self.renderedObjects[:]
        checkstate = 0
        
        for x in self.menu_options:
            if (checkstate == state):
                self.renderedObjects.append(self.fontchosen.render(x, 1, RED))
            else:
                self.renderedObjects.append(self.font.render(x,1,WHITE))
            checkstate += 1

        self.drawMenu()

    def numStates(self):
        return len(self.menu_options)
