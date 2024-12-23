import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 0.4
        self.musicVolume = 0.2
        self.targetMusicVolume = 0.2
        self.nextMusic = None
        self.currentMusic = None

        self.sounds = {
            'jump' : pygame.mixer.Sound('sounds/jump.wav'),
            'eat': pygame.mixer.Sound('sounds/healthrefill.wav'),
            'button' : pygame.mixer.Sound('sounds/button.wav'),
            'characterselect' : pygame.mixer.Sound('sounds/characterselect.wav'),
            'invis' : pygame.mixer.Sound('sounds/invis.wav'),
            'melee' : pygame.mixer.Sound('sounds/melee.mp3'),
            'hurt' : pygame.mixer.Sound('sounds/hurt.wav'),
            'pipe' : pygame.mixer.Sound('sounds/pipe_down.wav'),
            'win': pygame.mixer.Sound('music/bossclear.mp3')

        }
        self.music = {
            'menu': 'music/ChillMenu_Loopable.ogg',
            'lvl1' : 'music/KleptoLindaTitles_Loopable.ogg',
            'lvl2' : 'music/level2.ogg',
            'lvl3': 'music/level3.ogg',

        }
    def playSound(self, soundName):
        self.sounds[soundName].set_volume(self.soundVolume)
        self.sounds[soundName].play()

    def playMusic(self, musicName):

        #dont play music if already playing
        if musicName is self.currentMusic:
            return

        pygame.mixer.music.load(self.music[musicName])
        pygame.mixer.music.set_volume(self.musicVolume)
        self.currentMusic = musicName
        pygame.mixer.music.play(-1)

    def playMusicFade(self, musicName):

        #dont play music if already playing
        if musicName is self.currentMusic:
            return

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
                self.currentMusic = None
                self.musicVolume = 0
                pygame.mixer.music.set_volume(self.musicVolume)
                self.playMusic(self.nextMusic)
                self.nextMusic = None



