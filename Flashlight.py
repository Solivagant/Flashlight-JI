from pygame.locals import * #@UnusedWildImport
from fl.globals import * #@UnusedWildImport
from fl.base.Game import Game
from fl.base.Menu import Menu
from fl.base.Stat import Stat
from fl.net.Client import Client
from fl.net.Network import *
from threading import Condition
from fl.menu.OptionMenu import OptionMenu
from fl.net.Server import Server


'''
Created on 2009/12/26
Classe Mae do jogo.
Esta eh a classe que cria os objectos Game, Menu e Client
@author: gnascim@gmail.com
'''

class Main(object):
    '''Constructor da classe
       Cria um objecto Game, Menu e Network.
    '''   
    def __init__(self):
        global STATE_MENU, STATE_GAME, STATE_STATS
        STATE_MENU = 0
        STATE_GAME = 1
        STATE_STATS = 2
        pygame.init()
        #self.screen = pygame.display.set_mode((1024, 740),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1024, 700))
        pygame.display.set_caption("Flashlight")
        pygame.display.set_icon(load_image("flashlight.jpg", "res/img"))
        self.MainState = STATE_MENU
        self.ip = "localhost"
        self.port = 8740
        self.customization = False
        #criar o jogo
        self.game = Game(self.screen)
        self.menu = Menu(self.screen) 
        self.stat = Stat(self.screen)
        self.client = None
        
        self.audio = AudioResource()
        
        self.loop()
        os._exit(0)
        
    def loop(self):
        self.game.isMulti = False
        running = True
        while running:
            if(self.MainState==STATE_GAME):
                GameState = self.game.update()
                #Se for multiplayer
                if(self.game.isMulti==True):
                    #Tratar de msgs a enviar
                    if(self.game.SEND_MESSAGE):
                        if self.game.msg == "e":
                            print "MAIN catch 'e'"
                            self.client.treatOutgoing(self.game.msg)
                            quit()
                        else:
                            self.client.treatOutgoing(self.game.msg)
                            self.game.SEND_MESSAGE = False
                
                if(GameState==GAME_CONTINUE):
                    self.game.render()
                    
                elif(GameState==GAME_ESCAPE):
                    self.menu.set_game(True)
                    self.MainState = STATE_MENU
                    
                elif(GameState==GAME_STAT):
                    self.stat.update_stat(self.game.stat())
                    GameState = self.stat.update()
                    self.MainState = STATE_STATS
                                    
            elif(self.MainState==STATE_MENU):
                MenuState = self.menu.update()
                
                if(MenuState == START_SINGLE_GAME_EASY):
                    if not self.customization:
                        self.game.creation_player()
                        
                    #Carregar Audio Resource
                    self.audio.AddMusic('res/music/MusicAction.mp3', 'GameAction')
                    self.audio.get_music('GameAction').set_volume(0.5)
                    self.audio.get_music('GameAction').load_music()
                    pygame.mixer.music.play(-1)
                    
                    self.game.load_level("level1");
                    self.MainState = STATE_GAME
                    self.game.isMulti = False
                    self.game.creation_AI(2)
                elif(MenuState == START_SINGLE_GAME_MEDIUM):
                    if not self.customization:
                        self.game.creation_player()
                        
                     #Carregar Audio Resource
                    self.audio.AddMusic('res/music/MusicAction.mp3', 'GameAction')
                    self.audio.get_music('GameAction').set_volume(0.5)
                    self.audio.get_music('GameAction').load_music()
                    pygame.mixer.music.play(-1)
                       
                    self.game.load_level("level1");
                    self.MainState = STATE_GAME
                    self.game.isMulti = False
                    self.game.creation_AI(3)
                elif(MenuState == START_SINGLE_GAME_HARD):
                    if not self.customization:
                        self.game.creation_player()
                        
                    #Carregar Audio Resource
                    self.audio.AddMusic('res/music/MusicAction.mp3', 'GameAction')
                    self.audio.get_music('GameAction').set_volume(0.5)
                    self.audio.get_music('GameAction').load_music()
                    pygame.mixer.music.play(-1)
                    
                    self.game.load_level("level1");
                    self.MainState = STATE_GAME
                    self.game.isMulti = False
                    self.game.creation_AI(4)    
                if(MenuState == START_SERVER):
                    self.server = Server()
                    self.server.start()    
                if(MenuState == JOIN_SERVER):
                    if not self.customization:
                        self.game.creation_player()
                    #Carregar o nivel 1
                    
                    #Carregar Audio Resource
                    self.audio.AddMusic('res/music/MusicAction.mp3', 'GameAction')
                    self.audio.get_music('GameAction').set_volume(0.5)
                    self.audio.get_music('GameAction').load_music()
                    pygame.mixer.music.play(-1)
                    
                    self.game.load_level("level1");
                    self.MainState = STATE_GAME
                    self.game.isMulti = True
                    self.client = Client("cliente",self.game,self.ip, self.port)
                    self.game.set_client(self.client)
                
                if(MenuState == CHANGE_OPTIONS):
                    options = OptionMenu()
                    (option1, option2, option3, option4) = options.results

                    self.game.creation_player(option3, option2)
                    self.ip = option1
                    if option4.text != '':
                        self.port = int(option4.text)
                    self.customization = True
            elif(self.MainState==STATE_STATS):
                if self.stat.update() == GAME_CONTINUE:
                    self.MainState = STATE_GAME
Main()
