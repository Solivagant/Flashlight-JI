from fl.gameobject.GameObject import GameObject
from fl.globals import img


class crosshair(GameObject):

    # Constructor
    def __init__(self, (orig_x, orig_y)):
        GameObject.__init__(self, orig_x, orig_y,"Crosshair",1,((0,0, 9,7)),"crosshair.png", "res/img/")




