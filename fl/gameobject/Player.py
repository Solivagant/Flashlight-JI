from fl.audio.AudioResource import AudioResource
from fl.gameobject.GameObject import GameObject
from fl.globals import * #@UnusedWildImport
from fl.items import Weapon, Rifle, LaserRifle
from fl.items.Rifle import *
from fl.items.LaserRifle import *
from random import random
import random

class Player(GameObject):

    # Constructor
    def __init__(self, array, orig_x, orig_y,filename,name): 
        GameObject.__init__(self, orig_x, orig_y,name,6,((0,0, 32,28)),"boneco.png", "res/img" + "/" + filename)
        self.skin = filename
        self.jumping = False
        self.jumpingHorz = 0
        self.OnTheGround = False
        self.falling = True
        self.backupPos = orig_x, orig_y
        self.listControls = array
        self.weapon = Rifle()
        self.is_firing = 0
        self.dead = False
        #variavel de quantidade de salto feita por Carlos
        self.bla = 0
        self.shootingPosition = []
        self.shootingPosition.append(0)
        self.shootingPosition.append(0)
        #Player Audio Init
        self.playeraudio = AudioResource()
        self.playeraudio.AddSoundFXList([('res/music/footsteps.wav', 'footsteps'),
                                        ('res/music/laser.wav', 'laser'),
                                        ('res/music/gun_shotgun1.wav', 'gun_shotgun1'),
                                        ('res/music/reload.wav', 'reload'),
                                        ('res/music/pain_01.wav', 'pain_01'),
                                        ('res/music/blood_splat.wav', 'blood_splat'),
                                        ('res/music/gun_shell_drop.wav', 'shell')
                                        ])
        self.playeraudio.get_sound('footsteps').set_volume(0.4)
        
        #DIRECTION
        self.old_direction = LEFT
        self.moveX = 0
        self.moveY = 0 
        self.frameCurrent = FRAME_START
        
        #STAT PLAYER
        self.name = name
        self.bulletTotal = 0
        self.reload = 0
        self.playKilled = 0
        self.life = 100
        
        self.movement = (0,0,NONE)
        
        self.backupPosX = 0
        self.backupPosY = 0
        self.isMoving = False
           
    def get_controller(self):
        return self.array

    # Movimentos nos eixos X,Y
    def move(self, dx, dy):    
        # Chamamos primeiro o __move para o eixo dos XX, depois para os YY
        # para detectar colisoes melhor
        if dx != 0:             
            self.moveX = dx          
            self.__move(dx, 0)
        if dy != 0:             
            self.moveY = dy
            self.__move(0, dy)

    # Movimentos nos eixos X,Y
    def __move(self, dx, dy):

        self.position[0] += dx
        self.position[1] += dy
        
        self.update_position()
                    

    # Calcula a quantidade de movimento horizontal a usar em saltos e quedas
    # atraves das teclas left e right e da constante WALK_SPEED
    def horz_move_amt(self, input):
        return (input.held(self.listControls[1]) - input.held(self.listControls[0])) * WALK_SPEED


    def do_actions(self, input): 
        #Sound
        self.playeraudio.get_sound('footsteps').fadeout(3)
        self.moveX = 0
        self.moveY = 0 
        #Inputs/Actions
        #Esquerda   
        if input.held(self.listControls[0]) and not input.pressed(self.listControls[3]):
            
            self.isMoving = True
            
            if not self.OnTheGround:
                self.movement = (WALK_SPEED/2, 0, LEFT) 
            else:
                self.next_frame()
                self.movement = (WALK_SPEED, 0, LEFT)
            self.set_direction(LEFT)
        #Direita     
        elif input.held(self.listControls[1]) and not input.pressed(self.listControls[3]):
            
            self.isMoving = True
            
            if not self.OnTheGround:
                self.movement = (WALK_SPEED/2, 0, RIGHT) 
            else:
                self.next_frame()
                self.movement = (WALK_SPEED, 0, RIGHT)
            self.set_direction(RIGHT)
            
        #Salto
        elif input.pressed(self.listControls[3]):
            self.movement = (pygame.time.get_ticks(), self.horz_move_amt(input), UP)
            self.playeraudio.get_sound('footsteps').stop_sound()
        else:
            self.isMoving = False
            self.movement = (0,0,NONE)
            
        #Disparo
        if input.mouse_press(self.listControls[4]):
            self.reload = self.reload +1
            if self.reload < 10:  
                self.weapon.fire()
                self.is_firing = True
                self.playeraudio.get_sound('shell').play_sound()
                self.bulletTotal = self.bulletTotal + 1     
        else:
            self.is_firing = False
            
        if input.pressed(self.listControls[5]) or input.mouse_press(self.listControls[6]):
            self.playeraudio.get_sound('reload').play_sound()
            self.reset_reload()
            
        
        ###o resto dos saltos e quedas e tratado no Game
                    
    def render(self):   
        if self.is_firing == 1:
            self.image = self.images[0]
            if self.direction == RIGHT:
                self.image = self.revertImg[0]              
        else:
            if self.frameCurrent == 5:
                self.image = self.images[5]
                if self.direction == RIGHT:
                    self.image = self.revertImg[5]            
            elif self.frameCurrent == 10:
                self.image = self.images[4]
                if self.direction == RIGHT:
                    self.image = self.revertImg[4]            
            elif self.frameCurrent == 15:
                self.image = self.images[3]
                if self.direction == RIGHT:
                    self.image = self.revertImg[3]            
            elif self.frameCurrent == 20:
                self.image = self.images[2]
                if self.direction == RIGHT:
                    self.image = self.revertImg[2]            
            elif self.frameCurrent == FRAME_END:
                self.image = self.images[1]
                if self.direction == RIGHT:
                    self.image = self.revertImg[1]
            elif self.old_direction != self.direction:
                if self.direction == RIGHT:
                    self.image = self.revertImg[5]    

        #GFX, reiniciar a animacao
        if self.frameCurrent > FRAME_END:
            self.frameCurrent = FRAME_START
                      
    def dec_life(self, quantity):
        self.life = self.life - quantity;
        self.playeraudio.get_sound('pain_01').play_sound()
        if self.life <= 0:
            self.playeraudio.get_sound('blood_splat').play_sound()
            self.dead = True
            

    def get_life(self):
        return self.life;
    
    def get_name(self):
        return self.name
    
    def totalBullet(self):
        return self.bulletTotal
     
    def playersKilled(self):
        return self.playKilled
       
    def kill(self):
        GameObject.kill(self)
    
            
    def get_weapon(self):
        return self.weapon
        
    def pickup(self, Weapon):
        self.weapon = Weapon

    def next_frame(self):
        self.frameCurrent+=1
        
    def backupPosition(self):
        if self.moveX > 0:
            self.backupPosX = self.position[0]
        elif self.moveX < 0:
            self.backupPosX = self.position[0]
        else:
            self.backupPosX = self.position[0]
        self.backupPosY = self.position[1]
    
    def reset_movement(self):
        self.movement = (0,0,NONE)   
    
    def get_position(self):
        return self.position[0],self.position[1]
    
    def get_skin(self):
        return self.skin
    
    def get_reload(self):
        if self.reload > 10:
                return 1
        return 0
    
    def reset_reload(self):
        self.reload = 0
    
    def is_moving(self):
        return self.isMoving
    
    def set_moving(self,moving):
        self.moving = moving
        if self.moving == "False" :
            self.isMoving = False
        else:
            self.isMoving = True
    
    def get_direction(self):
        return self.direction
         
        