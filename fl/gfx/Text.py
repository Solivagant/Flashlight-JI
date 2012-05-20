from fl.Level import * #@UnusedWildImport
from fl.items.Bullet import * #@UnusedWildImport
from fl.gameobject.Crosshair import * #@UnusedWildImport
from fl.gameobject.Player import * #@UnusedWildImport
from fl.gameobject.Wall import * #@UnusedWildImport
from fl.gameobject.Life import * #@UnusedWildImport
from fl.gfx.Padlib import * #@UnusedWildImport
from fl.globals import * #@UnusedWildImport
from fl.inputListener import * #@UnusedWildImport
from pygame.locals import * #@UnusedWildImport

class Text():

    # Constructor
    def __init__(self,(orig_x, orig_y), text, size,type, color):
        self.color = color
        if type != None:
            self.font = pygame.font.Font("res/fonts/" + type, size)
        else:
            self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, 0,color)
        self.orig_x = orig_x;
        self.orig_y = orig_y;
        
    def get_position(self):
        return (self.orig_x, self.orig_y); 
    
    
    def get_name(self):
        return self.text
    
    def change_text(self,newText):
         self.text = self.font.render(str(newText), 0,self.color )
         
    
    
    


        
        