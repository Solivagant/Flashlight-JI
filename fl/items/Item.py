from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport

"""Classe base que define um objecto que os jogadores podem apanhar
-id (nome)
-imagem
-efeitos

"""
class Item(GameObject):
    def __init__(self, (orig_x, orig_y), name, sprite = "box.png"):
        GameObject.__init__(self, orig_x, orig_y+10,"Item",1,((0,0, 12,13)),sprite, "res/img/")
        self.toDelete = False
    def getName(self):
        return self.name
        