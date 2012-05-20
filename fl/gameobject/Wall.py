from fl.globals import * #@UnusedWildImport
from fl.gameobject.GameObject import GameObject

class Wall(GameObject):

    # Constructor
    def __init__(self, pos, texture, (width, height)):
        self.wallPos = []
        self.wallPos.append(pos[0])
        self.wallPos.append(pos[1])  
        GameObject.__init__(self, pos[0], pos[1],"Wall",1,((0,0, width,height)),texture, "res/img/tiles/")
      