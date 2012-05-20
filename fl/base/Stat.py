from fl.audio import AudioResource
from fl.globals import * #@UnusedWildImport
from fl.inputListener import * #@UnusedWildImport
from fl.gfx.Text import * #@UnusedWildImport
global screen, background, height, width

"""Gere o Menu inicial"""
class Stat(object):

    def __init__(self, screen):
        self.screen= screen
        self.background = load_image("stat_game.png", "res/img")
        self.input = inputListener()
        self.drawableTextLights = []
    
    def update_stat(self,list):
        self.drawableTextLights.append(Text((600,255),list[0], 26, None,(255,255,255)))    
        self.drawableTextLights.append(Text((600,300),list[1], 26, None,(255,255,255)))
        self.drawableTextLights.append(Text((600,350),list[2], 26, None,(255,255,255)))
        self.drawableTextLights.append(Text((600,400),list[3], 26, None,(255,255,255)))
        self.drawableTextLights.append(Text((600,450),list[4], 26, None,(255,255,255)))
        
    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.input.get_events()
        if self.input.pressed(K_TAB):
            return GAME_CONTINUE
        for text in self.drawableTextLights:
            self.screen.blit(text.get_name(),text.get_position())

        pygame.display.update()
        return GAME_STAT
        