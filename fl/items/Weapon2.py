from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport


class Weapon2(GameObject):
    
    def __init__(self, (orig_x, orig_y)):
        GameObject.__init__(self, orig_x, orig_y,"Weapon",6,((0,0,46,24)),"arms.png", "res/img/")
        
    def changeweapon(self,number):  
            self.image = self.images[number]
     
   