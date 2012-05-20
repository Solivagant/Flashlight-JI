from fl.audio import SoundFx, Music
import pygame

# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 8   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 60 # how often to check if playback has finished


class AudioResource(object):

    #Se type 0 e Musica se type 1 e Sound FX

    def __init__(self):

        #Start Sound FX Buffer com Objectos do tipo Sound
        self.SoundBuffer = []

        #Start Background Music Buffer com Objectos do tipo Music
        self.MusicBuffer = []

        pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)



    #Adiciona um novo Sound FX ao buffer dos Sound FX
    def AddSoundFX(self, path, name):
        self.SoundBuffer.append(SoundFx(path,name))

    #Adiciona um novo Music ao buffer dos Music
    def AddMusic(self, path, name):
        self.MusicBuffer.append(Music.Music(path,name))

    #Remove um Sound FX do Buffer
    def removeSoundFx(self, name):
        for x in self.SoundBuffer:
            if(name == x.getName()):
                self.SoundBuffer.remove(x)

    #Remove um Music do Buffer
    def removeMusic(self, name):
        for x in self.MusicBuffer:
            if(name == x.getName()):
                self.MusicBuffer.remove(x)

    #Recebe uma lista com tuplos (pathname, soundname)
    def AddSoundFXList(self, soundlist):
        try:
            for x in soundlist:
                self.SoundBuffer.append(SoundFx.SoundFx(x[0], x[1]))
        except pygame.error, message:
            print "Didn't find a specific Music File"
            raise SystemExit, message

    #Recebe uma lista com tuplos (pathname, musicname)
    def AddMusicList(self, musiclist):
        try:
            for x in musiclist:
                self.MusicBuffer.append(Music(x[0], x[1]))
        except pygame.error, message:
            print "Didn't find a specific Music File"
            raise SystemExit, message

    #Retorna um Sound Fx com nome X
    def get_sound(self, name):
        for x in self.SoundBuffer:
            if(x.get_name() == name):
                return x

    #Retorna um Music com nome X
    def get_music(self, name):
        for x in self.MusicBuffer:
            if(x.get_name() == name):
                return x
    