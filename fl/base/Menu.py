from fl.audio import AudioResource
from fl.globals import * #@UnusedWildImport
from fl.inputListener import * #@UnusedWildImport
from fl.menu.MenuCreator import cMenu
from fl.menu.menu_options import MENUSTART, MenuNewGame, MenuMulti, MenuOptions
import os

global screen, background, height, width

"""Gere o Menu inicial"""
class Menu(object):

    def __init__(self, screen):
        self.screen= screen
        self.background = load_image("fundo_menu.png", "res/img")

        self.menu = cMenu(MENUSTART, self.screen, self.background)

       
        path = '' + os.getcwd() + '/res/music/menu1.ogg'
        # criar recurso audio e fazer load do audio menu inicial e dos
        # efeitos menu
        self.audio = AudioResource.AudioResource()
        print "test"
        self.audio.AddMusic(path, 'menu1')
        print "test"

        self.audio.AddSoundFXList([(os.getcwd() + '/res/music/menuselect.wav', 'menuselect'),
                (os.getcwd() + '/res/music/gunshot.wav', 'gunshot'), ])
        print "test"

        #INICIALIZaCAO DAS VARIAVEIS DE ESTADO DO MENU E DO LISTENER
        self.input = inputListener()
        

        #Iniciar musica menu
        self.audio.get_music('menu1').load_music()
        pygame.mixer.music.play(-1)
        

        self.gameIsRunning = False
        
        self.state = 0
        self.menustate = (0, 'MAINMENU')
        self.maxstate = self.menu.numStates()        

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.input.get_events()
        self.menu.updateMenu(self.state)
        
        #SITEMA DE TROCA DE ESTADOS, VER QUAL E O ESTADO QUE ESTA O MENU
        if(self.input.pressed(K_DOWN)):
            self.audio.get_sound('menuselect').play_sound()
            if(self.state > self.maxstate - 2):
                self.state = 0
            else:
                self.state += 1

        elif(self.input.pressed(K_UP)):
            self.audio.get_sound('menuselect').play_sound()
            if (self.state < 1):
                self.state = self.maxstate - 1
            else:
                self.state -= 1

        #SISTEMA DE TROCA DE MENU ! SECALHAR METER NUM METODO APARTE !
        elif(self.input.pressed(K_RETURN) or self.input.mouse_press(1)):
            self.audio.get_sound('gunshot').play_sound()
            if(self.state == 0 and self.menustate[1] == 'MAINMENU'):
                self.menu = cMenu (MenuNewGame, self.screen, self.background)
                self.menustate = (1, 'NEWGAME')
                self.initStates()
            elif(self.state == 1 and self.menustate[1] == 'MAINMENU'):
                self.menu = cMenu (MenuMulti, self.screen, self.background)
                self.menustate = (1, 'MULTIMENU')
                self.initStates()
            elif(self.state == 2 and self.menustate[1] == 'MAINMENU'):
                self.menu = cMenu (MENUSTART, self.screen, self.background)
                self.menustate = (0, 'MAINMENU')
                self.initStates()
                return CHANGE_OPTIONS

            #SECCAO DOS CREDITS !!  
            elif(self.state == 3 and self.menustate[1] == 'MAINMENU'):
                pass
            ##TRATAR DO MULTIPLAYER - CREATE SERVER
            elif(self.state == 0 and self.menustate[1] == 'MULTIMENU'):
                pygame.mixer.music.fadeout(15)
                self.menustate = (0, 'MULTIMENU')
                return START_SERVER

            ##TRATAR DO MULTIPLAYER - JOIN SERVER
            elif(self.state == 1 and self.menustate[1] == 'MULTIMENU'):
                pygame.mixer.music.fadeout(15)
                self.menu = cMenu(MENUSTART, self.screen, self.background)
                self.menustate = (0, 'MAINMENU')
                self.initStates()
                return JOIN_SERVER

            elif(self.state == 0 and self.menustate[1] == 'NEWGAME'):
                pygame.mixer.music.fadeout(15)
                self.menustate = (0, 'MAINMENU')
                return START_SINGLE_GAME_EASY

            elif(self.state == 1 and self.menustate[1] == 'NEWGAME'):
                pygame.mixer.music.fadeout(15)
                self.menustate = (0, 'MAINMENU')
                return START_SINGLE_GAME_MEDIUM
            
            elif(self.state == 2 and self.menustate[1] == 'NEWGAME'):
                pygame.mixer.music.fadeout(15)
                self.menustate = (0, 'MAINMENU')
                return START_SINGLE_GAME_HARD            
            
            #TRATAMENTO DO MENU DE OPCOES
                 
            elif(self.state == 4 and self.menustate[1] == 'MAINMENU'):
                quit()

        #TRATA DOS EVENTOS DE ESCAPE KEY
        elif(self.input.pressed(K_ESCAPE)):
            if(self.menustate[0] == 1):
                self.menu = cMenu(MENUSTART, self.screen, self.background)
                self.menustate = (0, 'MAINMENU')
                self.initStates()

            elif(self.menustate[0] == 0 and self.gameIsRunning != True):
                quit()
            elif(self.menustate[0] == 0 and self.gameIsRunning == True):
                return BACK_TO_GAME

        pygame.display.update()


    #INICIA OS ESTADOS DO MENU
    def initStates(self):
        self.state = 0
        self.maxstate = self.menu.numStates()

    #Indica ao Menu se o Game esta a correr ou nao
    def set_game(self, bool):
        self.gameIsRunning = bool