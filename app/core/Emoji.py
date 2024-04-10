from cv2 import namedWindow, imread, imshow, waitKey, destroyAllWindows, WINDOW_FULLSCREEN, WINDOW_NORMAL, \
    setWindowProperty, WND_PROP_FULLSCREEN
import os
from time import sleep
from app.core import Constants
from app.core.Player import Player
from app.util.Dump import Dump
from app.util.Helper import Helper
from app.util.Setting import Setting


class Emoji:
    def run(self, feeling):
        Dump.dd('Running emoji...')
        current_feeling = feeling.value.decode("utf-8")
        screen = 'Animation'
        folder_path, image_files = self.load_new_emoji(feeling.value.decode("utf-8"))

        current_image = 0

        Dump.dd("Initiating frames...")
        while True:
            if current_feeling != feeling.value.decode("utf-8"):
                folder_path, image_files = self.load_new_emoji(feeling.value.decode("utf-8"))
                if not folder_path or len(image_files) <= 0:
                    folder_path, image_files = self.load_new_emoji('blink')
                current_feeling = feeling.value.decode("utf-8")
                current_image = 0
                Dump.dd('changed to: ' + current_feeling)

            image_path = os.path.join(folder_path, image_files[current_image])
            image = imread(image_path)
            imshow(screen, image)
            key = waitKey(40)
            if key == ord('q'):
                break
            current_image = (current_image + 1) % len(image_files)

        destroyAllWindows()

    def booting(self, feeling):
        Dump.dd('Running bootup...')
        screen = 'Animation'
        if Helper.is_raspberry():
            player = Player('storage/sounds/start.mp4')
            player.play_video()

            sleep(2)
            while player.is_playing():
                sleep(0.5)

        folder_path, image_files = self.load_new_emoji('loading')
        image_path = os.path.join(folder_path, image_files[0])
        image = imread(image_path)
        imshow(screen, image)
        if Helper.is_raspberry():
            player.release()
        Dump.dd('video finished, and start emoji now')

        feeling.value = bytes('loading', "utf-8")
        self.run(feeling)

    @staticmethod
    def load_new_emoji(current_feeling):
        folder_path = 'resources/emotions/' + current_feeling
        screen = 'Animation'
        image_files = []

        try:
            for filename in os.listdir(folder_path):
                if filename.endswith('.png') or filename.endswith('.jpg'):
                    image_files.append(filename)
            image_files.sort()
            namedWindow(screen, WINDOW_NORMAL)
            if Setting.config('full_screen'):
                setWindowProperty(screen, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
        except:
            pass

        return folder_path, image_files

    @staticmethod
    def change_emoji(feeling):
        new_feeling = bytes(feeling, "utf-8")
        if Constants.feeling and Constants.feeling.value == new_feeling:
            return

        Dump.dd('Setting new feeling: ' + feeling)
        Constants.feeling.value = new_feeling

        sound = 'storage/sounds/' + feeling + '.mp3'

        if os.path.isfile(sound):
            player = Player(sound)
            player.play_audio()
            sleep(1)
            while player.is_playing():
                sleep(1)
            player.release()
