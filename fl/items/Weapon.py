from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport
from fl.items import Item
from fl.items.Item import *
from fl.audio.AudioResource import *
"""Classe base que define uma arma que os jogadores podem apanhar
-id (nome)
-imagem
-efeitos

"""

class Weapon(Item):
    #Os atributos com None ainda nao estao a ser atribuidos nem usados nesta classe.
    def __init__(self, name, bullet, sound, sprite = "box.png", (pos_x, pos_y) = (0,0), range = None, ilumination = None, burnout = None, fireRate = None, dmg = None, areaOfEffect = None, ammoSprite = None):
        self.name = name
        self.bullet = bullet
        self.sound = sound
        self.audio = AudioResource()
        self.audio.AddSoundFXList([('res/music/'+sound+'.wav', sound),
                                        ('res/music/gun_shell_drop.wav', 'shell')])  
  
        #Item.init(self, (0,0), (0,0), , name, sprite)
        #Defining the Parameter Specific to the Weapon Type Objects
        self.name = name
        self.range = range
        self.ilumination = ilumination  #Boolean that specifies if the ammunition iluminates the dark
        self.burnout = burnout # How Long it takes to burn out the light of the weapon once it reaches its destination
        self.fireRate = fireRate # 0 - Slow, 1 - Normal, 2 - Fast
        self.dmg = dmg  #How much damage the weapon does, if a player is hit with
                        #subtract the total of his current life with this modifier
        
        self.areaOfEffect = areaOfEffect  #0 - No Area of Effect, 1 - Area of Effect of 5 or so pixels
        self.ammoSprite = ammoSprite  
        
        
    def fire(self):
            self.audio.get_sound(self.sound).play_sound()
    
  

        