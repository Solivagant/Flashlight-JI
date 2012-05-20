import math
import pygame, os
#CONSTANTES PARA O JOGO: FLAGS E VALORES NOMINAIS
#PARA VELOCIDADES DE MOVIMENTO, BALAS, ETC

#SALTOS
JUMPING_DURATION =  400    #Duracao dos Saltos (millisegundos)
JUMP_HEIGHT = 8           #Altura do Salto (pixeis)
FALL_SPEED = 5             #Rapidez da queda (pixeis)
#Tempo que fica ao maximo de altura do salto (usado nos calculos)
TIME_AT_PEAK = JUMPING_DURATION / 2

#MOVIMENTOS
WALK_SPEED = 6 #Velocidade ao andar (pixeis)
UP = 2         #Saltar
RIGHT = 1      #Andar para a direita
LEFT = -1      #Andar para a esquerda
NONE = 0       #Sem movimento

#VELOCIDADE DAS BALAS
BULLET_SPEED = 0.40

WALL_WIDTH = 32
WALL_HEIGHT = 34
Screen = (1024,700)
PLAYER_SHOOTS = 1
PLAYER_IDLE = 0

#Distancia maxima a que o rato pode tar do jogador
MAX_DISTANCE = 10

#Distancia minima a que o rato pode tar do jogador
MIN_DISTANCE = 2

## RGB color for Black
BLACK = (0, 0, 0)

## RGB color for White
WHITE = (255, 255, 255)

## RGB color for Red
RED = (255, 0, 0)

## RGB color for Green
GREEN = (0, 255, 0)

## RGB color for Blue
BLUE = (0, 0, 255)

PASSOS = 0

#Globais para as frames de renderizacao dos sprites (util mesmo para as spritesheets espero eu)
FRAME_START = 1
FRAME_END = 25

#network globals
ONLINE = 111
OFFLINE = 010

#CONSTANTES PARA O MAIN
START_SINGLE_GAME_EASY = 1
START_SINGLE_GAME_MEDIUM = 11
START_SINGLE_GAME_HARD = 111
START_SERVER = 2
JOIN_SERVER = 6
GAME_STAT = 4
QUIT = 3
BACK_TO_GAME = 4
CHANGE_OPTIONS = 7

#CONSTANTES PARA O GAME
GAME_CONTINUE = 0
GAME_ESCAPE = 1

img = "images/"
player1_img = "player_one/"
player2_img = "player_two/"

def distance((x1,y1), (x2, y2)):
    return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))


"""Carrega uma imagem a partir da pasta indicada"""
def load_image(file_name, folder, colorkey = None):
    full_name = os.path.join(folder, file_name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error, message:
        print 'Cannot load image:', full_name
        raise SystemExit, message
    
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image