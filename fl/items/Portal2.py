from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport

"""Classe base que define um objecto que os jogadores podem apanhar
-id (nome)
-imagem
-efeitos

"""
class Portal2(GameObject):
    def __init__(self, (orig_x, orig_y), name, sprite = "portal2.png"):
        GameObject.__init__(self, orig_x, orig_y+7,"Portal2",1,((0,0, 86,80)),sprite, "res/img/")
        self.toDelete = False
    def getName(self):
        return self.name