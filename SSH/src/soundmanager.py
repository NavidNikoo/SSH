import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 0.4
        self.musicVolume = 0.2
        self.targetMusicVolume = 0.2
        self.nextMusic = None

        self.sounds = {
            'jump' : pygame.mixer.Sound('sounds/jump.wav'),
            'eat': pygame.mixer.Sound('sounds/healthrefill.wav'),
        }
        self.music = {
            'game' : 'music/KleptoLindaTitles_Loopable.ogg',
            'menu' : 'music/ChillMenu_Loopable.ogg'
        }
    def playSound(self, soundName):
        self.sounds[soundName].set_volume(self.soundVolume)
        self.sounds[soundName].play()
    def playMusic(self, musicName):
        pygame.mixer.music.load(self.music[musicName])
        pygame.mixer.music.set_volume(self.musicVolume)
        pygame.mixer.music.play(-1)

    def playMusicFade(self, musicName):
        self.nextMusic = musicName
        self.fadeOut()

    def fadeOut(self):
        pygame.mixer.music.fadeout(500)

    def update(self):
        #raise volume
        if self.musicVolume < self.targetMusicVolume:
            self.musicVolume = min(self.musicVolume + .005, self.targetMusicVolume)
            pygame.mixer.music.set_volume(self.musicVolume)

        #play next music if appropriate
        if self.nextMusic is not None:
            # if old music has finished fading out
            if not pygame.mixer.music.get_busy():
                self.musicVolume = 0
                pygame.mixer.music.set_volume(self.musicVolume)
                self.playMusic(self.nextMusic)
                self.nextMusic = None


