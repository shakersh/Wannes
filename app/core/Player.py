import vlc
from app.util.Helper import Helper
from app.util.Setting import Setting
import pygame


class Player:

    def __init__(self, video):
        if Helper.is_raspberry():
            self.player = vlc.MediaPlayer(video)
        else:
            pygame.mixer.init()
            self.player = pygame.mixer.music

        self.video = video

    def play_video(self, is_video=True):
        if Helper.is_raspberry():
            if Setting.config('full_screen') and is_video:
                self.player.set_fullscreen(True)

            self.player.play()
            self.player.pause()
        else:
            # Loading the song
            self.player.load(self.video)

        # Start playing the sound
        self.player.play()

    def play_audio(self):
        self.play_video(is_video=False)

    def is_playing(self):
        if Helper.is_raspberry():
            return self.player.is_playing()

        return self.player.get_busy()

    def release(self):
        if Helper.is_raspberry():
            self.player.release()
        else:
            pygame.mixer.quit()
