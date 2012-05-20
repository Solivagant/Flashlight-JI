'''
Created on 2009/11/22
Levels
@author: Solivagant

informacao a guardar nos niveis:
-arquitectura
-texturas das paredes, portas
-imagem do fundo
-sons especificos
-musicas de fundo
-items no nivel
-inimigos
-posicoes dos jogadores (aqui ou no Game)
'''
from fl.gameobject.Wall import Wall
from fl.globals import * #@UnusedWildImport
from fl.items.Item import Item
from fl.items.Portal import Portal
from fl.items.Portal2 import Portal2
from fl.gameobject.Ladder import Ladder
from fl.RespawnPoint import RespawnPoint

class Level(object):

    def __init__(self, filename):  
        self.filename = filename;
        self.load_file();

    def load_file(self):
        #abrir o ficheiro com os dados do nivel
        file = open("res/levels/" + self.filename, 'rb', 1)

        #nome do nivel
        temp = file.next()
        self.name = temp.split('\"')[1]
        
        #bg do nivel
        temp = file.next()
        bg = temp.split('\"')[1]
        self.bg = load_image(bg, "res/img")

        #textura das paredes
        temp = file.next()
        wall_text = temp.split('\"')[1]
        temp = file.next()
        wall_text_semrelevo = temp.split('\"')[1]        
        temp = file.next()
        wall_text_direito = temp.split('\"')[1]
        temp = file.next()
        wall_text_esquerdo = temp.split('\"')[1]
        #textura do fundo
        temp = file.next()
        bg_text = temp.split('\"')[1] 
                            
        #tamanho e comprimento de cada quadrado
        temp = file.next()
        height = int(temp.split('\"')[1])

        temp = file.next()
        width = int(temp.split('\"')[1])
                
        self.walls = []
        self.items = []
        self.portals = []
        self.bg_tiles = []
        self.respawn = []
        self.Occluders = []
        self.ladders = []
        shadow_map = []
        level = []
        
        #iterar sobre as linhas do ficheiro
        for line in file:
            split = line.split('\"')
            level.append(split[0])
            shadow_map.append(split[1])

        x = y = 0
        for row in shadow_map:
            for col in row: 
                if col == "V":
                    #Se eh parede vertical, quero posicionar as sombras a width 1 e que cubram a altura toda
                    self.Occluders.append(pygame.Rect(x, y - (height/2), 1, height+1))
                if col == "H":
                    #Se eh parede horizontal, quero posicionar as sombras na totalidad do witdh da parede e que cubram altura de 1
                    self.Occluders.append(pygame.Rect(x - 16, y, width, 1))
                    
                if col == "C":
                    #Se eh canto direito inferior, quero por uma mistura dos dois
                    self.Occluders.append(pygame.Rect(x - 16, y, width-16, 1))
                    self.Occluders.append(pygame.Rect(x, y - (height/2), 1, height-15))
                if col == "K":
                    #Se eh canto direito superior, quero por uma mistura dos dois
                    self.Occluders.append(pygame.Rect(x - 16, y, width-16, 1))
                    self.Occluders.append(pygame.Rect(x, y, 1, height+15))
                
                if col == "X":
                    #Se eh canto esquerdo inferior, quero por uma mistura dos dois
                    self.Occluders.append(pygame.Rect(x, y, width, 1))
                    self.Occluders.append(pygame.Rect(x, y - (height/2), 1, height-15))                 
                if col == "Q":
                    #Se eh canto esquerdo superior, quero por uma mistura dos dois
                    self.Occluders.append(pygame.Rect(x, y, width, 1))
                    self.Occluders.append(pygame.Rect(x, y, 1, height+15))
                    
                #if col == "T":
                    #se eh um T:
                #    self.Occluders.append(pygame.Rect(x - 16, y, width-16, 1))
                #    self.Occluders.append(pygame.Rect(x, y - (height/2), 1, height-15))                    
                if col == "R":
                    #Se eh um terminador de parede horizontal de direita, quero desenhar sombra ate meio
                    self.Occluders.append(pygame.Rect(x - 16, y, width/2, 1))
                if col == "E":
                    #Se eh um terminador de parede horizontal de esquerda, quero desenhar sombra ate meio
                    self.Occluders.append(pygame.Rect(x, y, width/2, 1))                                       
                x += width
            y += height 
            x = 0       

        x = y = 0
        count = 0
        for row in level:
            for col in row:
                if col == "W":
                    self.walls.append(Wall((x, y),wall_text,(width, height)))
                #Parede sem relevo
                if col == "S":
                    self.walls.append(Wall((x, y),wall_text_semrelevo,(width, height)))
                #Parede lado direito
                if col == "D":
                    self.walls.append(Wall((x, y),wall_text_direito,(width, height)))
                #Parede lado equerdo
                if col == "E":
                    self.walls.append(Wall((x, y),wall_text_esquerdo,(width, height)))
                if col == "I":
                    self.items.append(Item((x,y),"item"+str(count)))
                    count +=1
                if col == "P":#Portal(entradas)
                    self.items.append(Portal((x,y),"item"+str(count)))
                    count +=1
                if col == "p":#Portal(saidas)
                    self.items.append(Portal2((x,y),"item"+str(count)))
                    count +=1
                if col == "R":
                    self.respawn.append(RespawnPoint(x,y))
                if col == "L":
                    self.ladders.append(Ladder((x,y),(width,height)))
                x += width
            y += height
            x = 0

        #fechar o file
        file.close()
    
    def getWalls(self):
        return self.walls
    
    def getOccluders(self):
        return self.Occluders
    
    def getItems(self):
        return self.items
    def getPortals(self):
        return self.portals
    
    def getBGTiles(self):
        return self.bg_tiles
    
    def getLadders(self):
        return self.ladders
