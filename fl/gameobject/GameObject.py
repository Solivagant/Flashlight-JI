from fl.globals import *
import pygame.sprite
from fl.gfx.Sprites import *

class GameObject(pygame.sprite.Sprite):


    """Extensao da classe Sprite, classe geral para ser extendida por todas as classes de objectos
    """
           
    def __init__(self, x, y,name,number_img,rectangle, image_name, image_path):
        
        self.name = name
        self.delete = False
        pygame.sprite.Sprite.__init__(self)
        spr = Sprites(image_path + "/" +  image_name)
        self.images = []

        #self.images = spr.images_at(rectangle, colorkey=(255, 255, 255))
        self.images = spr.load_strip(rectangle,number_img, colorkey=(255, 255, 255))
        self.image = self.images[0]
        self.revertImg = []
        for img in self.images:
            self.revertImg.append(pygame.transform.flip(img,1,0))
        self.position = []
        self.position.append(x)
        self.position.append(y)
        self.direction = LEFT
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.direction = LEFT

                   
    def update_position(self):
        """Updates the (visible) position of the sprite."""
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    
    def set_direction(self, new_direction):
        self.old_direction = self.direction
        self.direction = new_direction

    def set_reverse_direction(self):
        self.old_direction = self.direction
        if self.direction == LEFT:
            self.direction = RIGHT
        else:
            self.direction = LEFT
        
    def render(self):
        if self.direction != self.old_direction:
            if self.direction == RIGHT:
                self.originalImage = self.image_right
                self.image = self.originalImage
            elif self.direction == LEFT:
                self.originalImage = self.image_left
                self.image = self.originalImage
                
    def schedule_delete(self):
        self.delete = True