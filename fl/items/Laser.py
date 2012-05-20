from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport
from test.double_const import PI

class Laser(GameObject):

    # Constructor
    def __init__(self, (orig_x, orig_y), (target_x, target_y), owner):
        GameObject.__init__(self, orig_x, orig_y,"Laser",1,((0,0, 7,2)),"laser.png", "res/img/bullets")
        self.target = (target_x, target_y)
        self.damage = 10
        self.bullet_speed = 0.40
        self.owner = owner
        #rodar a imagem da bullet em relacao ao alvo
        self.image = pygame.transform.rotate(self.image, (math.atan2(orig_y - target_y, target_x - orig_x) * 180 / PI))
        
        #incrementos de X e Y para o movimento da bala
        if(self.target[0]>self.position[0]):
            self.moveX = ((self.target[0]-self.position[0])*self.bullet_speed)
        else:
            self.moveX = -((self.position[0]-self.target[0])*self.bullet_speed)
        if(self.target[1]>self.position[1]):
            self.moveY = ((self.target[1]-self.position[1])*self.bullet_speed)
        else:
            self.moveY = -((self.position[1]-self.target[1])*self.bullet_speed)
        
        self.moving = 1
        
    # Movimentos nos eixos X,Y
    def move(self, dx, dy):

        # Chamamos primeiro o __move para o eixo dos XX, depois para os YY
        # para detectar colisoes melhor
        if dx != 0:
            self.__move(dx, 0)
        if dy != 0:
            self.__move(0, dy)

    # Movimentos nos eixos X,Y
    def __move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

        self.update_position()

    def update(self):
        if(self.moving==1):
            self.move(self.moveX, self.moveY)

    def render(self):
        self.image = self.image
