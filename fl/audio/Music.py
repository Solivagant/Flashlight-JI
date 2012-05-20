import pygame

class Music(object):

    #Inicializa um objecto do tipo Music
    def __init__(self, path, name):

        self.name = name
        self.path = path

    #Faz load da musica
    def load_music(self):
        try:
            pygame.mixer.music.load(self.path)

        except pygame.error, message:
            print "Didn't find the specific Music File"
            raise SystemExit, message

    #Adiciona a musica a queue
    def add_queue(self):
        try:
            pygame.mixer.music.queue(self.path)

        except pygame.error, message:
            print "Didn't find the specific Music File"
            raise SystemExit, message
        
    
    #Set Volume of the Music
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    #Retorna o nome do objecto musica
    def get_name(self):
        return self.name


