from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport
from fl.items import Item, Weapon
from fl.items.Weapon import *
from fl.items.Laser import Laser
"""Classe base que define uma arma que os jogadores podem apanhar
-id (nome)
-imagem
-efeitos

"""

class LaserRifle(Weapon):
    def __init__(self):
        Weapon.__init__(self,"laserrifle", "laser", "laser")
    def new_bullet(self, (x, y), (cx, cy), owner ):
        return Laser((x, y), (cx, cy), owner)
