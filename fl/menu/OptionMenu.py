import pygame
from pygame import font
from fl.globals import * #@UnusedWildImport
from fl.gfx.Sprites import *
import gui
from gui import *

#PYGAME INITIALIZATION AND EXTRA STUFF

class OptionMenu(object):

    def __init__(self):

        self.run = True
        import defaultStyle
        defaultStyle.init(gui)
        self.screen = pygame.display.set_mode((1024, 700))
        #First, we create a desktop to contain all the widgets
        self.desktop = Desktop()
        self.background = load_image("fundo_menu.png", "res/img")
        #IMPORTANTE RESULTADO FINAL
        self.playername = ""
        self.ip_server = ""
        self.port_server = ""
        self.player_folder = ""
        
        
        self.animation_player = 0
        self.a = 0 
        self.p1 = []
        self.p2 = []
        self.p3 = []
        self.p4 = []
        self.p5 = []
        self.p6 = []
        
        self.addPlayerImages()
        self.createOptionMenu()
       
    
        
        return self.gameLoop()
     
                   
    def createOptionMenu(self):
        title_text = gui.defaultLabelStyle.copy()
        title_text['font'] = pygame.font.Font(None,40)
        
        normal_text = gui.defaultLabelStyle.copy()
        normal_text['font'] = pygame.font.Font(None,20)
        
        
        label = Label(position = (490,230),size = (1,1), parent = self.desktop, text = "OPTIONS",style = normal_text)
        label = Label(position = (370,270),size = (1,1), parent = self.desktop, text = "Player Name:",style = normal_text)
        label = Label(position = (370,300),size = (1,1), parent = self.desktop, text = "Server Hostname:",style = normal_text)
        label = Label(position = (370,330),size = (1,1), parent = self.desktop, text = "Port Name:",style = normal_text)
        
        
        self.playername = TextBox(position = (500,270), size = (180, 0), parent = self.desktop, text = "")
        self.ip_server = TextBox(position = (500,300), size = (180, 0), parent = self.desktop, text = "")
        self.port_server = TextBox(position = (500,330), size = (100, 0), parent = self.desktop, text = "")

        #OptionBox(position = (500,300),size = (1,1),parent = self.desktop, text = "Option 1", value = True)
        #OptionBox(position = (500,300), parent = self.desktop, text = "Option 2")
        #OptionBox(position = self.desktop.nextPosition(4), parent = self.desktop, text = "Option 3")
        
        button = Button(position = (439,480), size = (200,0), parent = self.desktop, text = "Save Settings")
        
        button1 = Button(position = (390,375), size = (10,10), parent = self.desktop, text = "1")
        button2 = Button(position = (490,375), size = (10,10), parent = self.desktop, text = "2")
        button3 = Button(position = (590,375), size = (10,10), parent = self.desktop, text = "3")
        button4 = Button(position = (390,410), size = (10,10), parent = self.desktop, text = "4")
        button5 = Button(position = (490,410), size = (10,10), parent = self.desktop, text = "5")
        button6 = Button(position = (590,410), size = (10,10), parent = self.desktop, text = "6")
           
        button.onClick = self.buttonOnClick
        button1.onClick = self.buttonOnClick2
        button2.onClick = self.buttonOnClick3
        button3.onClick = self.buttonOnClick4
        button4.onClick = self.buttonOnClick5
        button5.onClick = self.buttonOnClick6
        button6.onClick = self.buttonOnClick7
        
    def buttonOnClick(self,button):
        self.run = False
        self.results = (self.ip_server.text,self.playername.text,self.player_folder, self.port_server)
    
    def buttonOnClick2(self,button):
        self.player_folder = "player_one"
    
    def buttonOnClick3(self,button):
        self.player_folder = "player_two"
    
    def buttonOnClick4(self,button):
        self.player_folder = "player_three"
    
    def buttonOnClick5(self,button):
        self.player_folder = "player_four"
    
    def buttonOnClick6(self,button):
        self.player_folder = "player_five"
        
    def buttonOnClick7(self,button):
        self.player_folder = "player_six"
        
    def addPlayerImages(self):
        self.p1 = self.imageBoxPosition(Sprites("res/img/player_one/boneco.png"), (400,370))
        self.p2 = self.imageBoxPosition(Sprites("res/img/player_two/boneco.png"), (500,370))
        self.p3 = self.imageBoxPosition(Sprites("res/img/player_three/boneco.png"), (600,370))
        self.p4 = self.imageBoxPosition(Sprites("res/img/player_four/boneco.png"), (400,410))
        self.p5 = self.imageBoxPosition(Sprites("res/img/player_five/boneco.png"), (500,410))
        self.p6 = self.imageBoxPosition(Sprites("res/img/player_six/boneco.png"), (600,410))
                
    def imageBoxPosition(self,spr,pos):
        player_movie = []
        player_movie = spr.load_strip((0,0, 32,28),6, colorkey=(255, 255, 255))
        newList = []
        for player_img in player_movie:
            newList.append((player_img,pos))
        return newList
    
    def animation_players(self):
             
            if self.animation_player > 0 and self.animation_player <5: 
                self.a = 0  
            if self.animation_player > 5 and self.animation_player < 10: 
                self.a = 1  
            if self.animation_player > 10 and self.animation_player < 15: 
                self.a = 2 
            if self.animation_player > 20 and self.animation_player < 25: 
                self.a = 3 
            if self.animation_player > 25 and self.animation_player < 35: 
                self.a = 4
            if self.animation_player == 35: 
                self.animation_player = 0   
                self.a = 0 
            self.animation_player = self.animation_player+1
            
                    
    def gameLoop(self):
        while self.run: 
            #Just for exit        
            for e in gui.setEvents(pygame.event.get()):
                if e.type == pygame.QUIT:
                    self.run = False
            
            self.desktop.update()
            #Here begins rendering
            self.screen.fill((20,40,50))               

            self.screen.blit(self.background, (0,0))
            
            #Animacao dos bonecos:
            self.animation_players()
           
            self.screen.blit(self.p1[self.a][0],self.p1[self.a][1])    
            self.screen.blit(self.p2[self.a][0],self.p2[self.a][1])
            self.screen.blit(self.p3[self.a][0],self.p3[self.a][1])
            self.screen.blit(self.p4[self.a][0],self.p4[self.a][1])
            self.screen.blit(self.p5[self.a][0],self.p5[self.a][1])
            self.screen.blit(self.p6[self.a][0],self.p6[self.a][1])
            
            
            
                
            self.desktop.draw()
            #Flips!
            pygame.display.flip()  

