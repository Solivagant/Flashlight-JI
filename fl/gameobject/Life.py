from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport


class Life(GameObject):
    
    def __init__(self, (orig_x, orig_y)):
        GameObject.__init__(self, orig_x, orig_y,"Life",1,((0,0, 100,15)),"life.png", "res/img/")
        self.tempo_aux = 1
        
                    
    def loseLife(self, damage):
        if self.tempo_aux < 100 and self.tempo_aux >= 1:
            self.image = pygame.transform.scale(self.image,(100-self.tempo_aux,15))
            self.tempo_aux+=damage
            
    def restoreLife(self):
        self.image = pygame.transform.scale(self.image,(100,15))
     
    
 
    
           
        
        
