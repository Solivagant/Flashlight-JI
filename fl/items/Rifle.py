from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport
from fl.items import Item, Weapon
from fl.items.Weapon import *
from fl.items.Bullet import Bullet
"""Classe base que define uma arma que os jogadores podem apanhar
-id (nome)
-imagem
-efeitos

"""

class Rifle(Weapon):
    def __init__(self):
        Weapon.__init__(self,"rifle", "bullet", "gun_shotgun1")
    def new_bullet(self, (x, y), (cx, cy), owner ):
        return Bullet((x, y), (cx, cy), owner)