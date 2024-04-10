from datetime import datetime
from app.util.Setting import Setting
from gtts import gTTS
from io import BytesIO
import pygame


class Dump:
    @staticmethod
    def dd(*values):
        if Setting.config('debug'):
            driver = Setting.config('log_driver')
            for value in values:
                output_function = getattr(Dump, driver)
                output_function(value)

    @staticmethod
    def screen(value):
        print(value)

    @staticmethod
    def sound(value):
        print(value)

        if isinstance(value, str):
            mp3_fp = BytesIO()
            obj = gTTS(text=value, lang='en')
            obj.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            pygame.mixer.init()
            sound = pygame.mixer.music

            sound.load(mp3_fp)
            sound.play()

            while sound.get_busy():
                continue

    @staticmethod
    def file(value):
        print(value)

        with open('storage/logs/log.log', 'a', encoding="utf-8") as f:
            f.write(datetime.now().strftime("%H:%M:%S.%f")[:-3] + ":\t" + str(value) + "\n")
