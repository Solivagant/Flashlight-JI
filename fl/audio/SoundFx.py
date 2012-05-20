import pygame

class SoundFx(object):

    #Inicializa um novo Sound FX
    def __init__(self, path, name):

        self.name = name

        try:
            self.sound = pygame.mixer.Sound(path)
        except pygame.error, message:
            print "Didn't find a specific Sound Fx File"
            raise SystemExit, message

    #Plays Sound
    def play_sound(self):
        self.sound.play()

    #Retorna o tamanho do Sound
    def sound_length(self):
        return self.sound.get_length

    #Define o volume do som ( Valores entre 0.0 e 1.0 )
    def set_volume(self, num):
        self.sound.set_volume(num)

    #Faz fadeout de um som em x milisegundos
    def fadeout(self, time):
        self.sound.fadeout(time)

    #O Som para de Tocar
    def stop_sound(self):
        self.sound.stop()

    #Retorna o nome do som
    def get_name(self):
        return self.name

    