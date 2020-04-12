import pygame.event
from pygame.locals import * #@UnusedWildImport

""" Listener para eventos de Input
    para teclado e rato
"""
class inputListener(object):
    QUIT = 0
    DOWN = 1
    UP = 2
    HELD = 3
    MOUSEMOTION = 4
    

    def __init__(self):
        
        #Sair do Jogo
        self.toQuit = False
        
        #Dicionario para os inputs
        self.inputs = {}

    """ Fetch aos eventos no pygame """
    def get_events(self):
        """limpar eventos up ja existentes no dictionary de inputs
           nomeadamente eventos UP em que a tecla tinha sido largada
           no ciclo anterior
        """
        self.mouse_moved = False
        toDelete = []
        for key in self.inputs:
            if(self.inputs.get(key, -1) == self.UP):
                """ marcar para apagar
                (nao e boa ideia apagar items duma lista quando estamos a iterar sobre ela)
                """
                toDelete.append(key)
                """se ja existe no dictionary esta tecla carregada para baixo,
                   significa que ja estava pressionada no ciclo anterior, logo
                   atribuimos o estado HELD
                """
            elif(self.inputs.get(key, -1)==self.DOWN):
                self.inputs.update({key: self.HELD})

        for key in toDelete:
            del self.inputs[key]
            
        for event in pygame.event.get():
            input = 0
            if event.type == pygame.QUIT:
                pygame.quit();
            elif event.type == KEYDOWN:
                if not self.inputs.get(event.key, -1)==self.HELD:
                    input = {event.key: self.DOWN}
            elif event.type == KEYUP:
                input = {event.key: self.UP}
            elif event.type == MOUSEBUTTONDOWN:
                input = {event.button : self.DOWN}
            elif event.type == MOUSEBUTTONUP:
                input = {event.button : self.UP}
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_moved = True

            if(input!=0):
                self.inputs.update(input)

    def released(self, key):
        return self.inputs.get(key, -1) == self.UP

    def held(self, key):
        return self.inputs.get(key, -1) == self.HELD

    def pressed(self, key):
        return self.inputs.get(key, -1) == self.DOWN

    def mouse_press(self, button):
        return self.inputs.get(button, -1) == self.UP

    def mouse_moved(self):
        return self.mouse_moved
    
    def toQuit(self):
        return self.toQuit

