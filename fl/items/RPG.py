'''
Created on 2010/01/08

@author: Solivagant
'''
from fl.items.Rocket import Rocket
from fl.items.Weapon import Weapon
class RPG(Weapon):
    def __init__(self):
        Weapon.__init__(self,"rpg", "rocket", "rocket")
    def new_bullet(self, (x, y), (cx, cy) , owner):
        return Rocket((x, y), (cx, cy),owner)