from datetime import datetime
from io import BytesIO
from gtts import gTTS
import pygame
import speech_recognition as recognition
from app.core.Emoji import Emoji
from app.util.Setting import Setting
from app.util.Dump import Dump
from app.core import Constants


class Audio:

    @staticmethod
    def split_text(text):
        first_list = text.split('.')

        second_list = []
        for paragraph in first_list:
            second_list = second_list + paragraph.split(',')

        final_list = []
        for paragraph in second_list:
            final_list = final_list + paragraph.split('،')

        while ("" in final_list):
            final_list.remove("")

        return final_list

    def stream(self, paragraphs, with_emoji):
        mp3_fp = BytesIO()
        text = paragraphs.pop(0)

        obj = gTTS(text=text, lang='ar')
        obj.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        pygame.mixer.pre_init(30000, -16, 2, 2048)
        pygame.mixer.init()
        sound = pygame.mixer.music

        if with_emoji:
            Emoji.change_emoji('speak')

        sound.load(mp3_fp)
        sound.play()

        Dump.dd('start playing at: ' + datetime.now().strftime("%H:%M:%S.%f")[:-3])
        Dump.dd(text, paragraphs)
        sounds_list = []
        while len(paragraphs):
            tmp = BytesIO()
            text = paragraphs.pop(0)
            obj = gTTS(text=text, lang='ar')
            obj.write_to_fp(tmp)
            tmp.seek(0)
            sounds_list.append(tmp)
            Dump.dd(text, paragraphs)

            if not sound.get_busy():
                sound.load(sounds_list.pop(0))
                sound.play()
                Dump.dd('Still loading, then play the second part')

        self.play_back(sound, sounds_list)

        pygame.mixer.quit()

    def play_back(self, sound, sounds_list):
        while sound.get_busy():
            continue

        if len(sounds_list):
            next_audio = sounds_list.pop(0)
            sound.load(next_audio)
            sound.play()
            self.play_back(sound, sounds_list)

    def speak(self, text, with_emoji=True):
        Dump.dd('got at: ' + datetime.now().strftime("%H:%M:%S.%f")[:-3])
        paragraphs = self.split_text(text)
        Dump.dd(paragraphs)
        Dump.dd('splitted at: ' + datetime.now().strftime("%H:%M:%S.%f")[:-3])

        self.stream(paragraphs, with_emoji)
        Dump.dd('end playing at: ' + datetime.now().strftime("%H:%M:%S.%f")[:-3])

    def listen(self, tries=0, with_emoji=True):
        if with_emoji:
            Emoji.change_emoji('blink')
        mode = Setting.config('mode')
        request = None
        try:
            with recognition.Microphone() as source:
                Dump.dd(f"I am listening..., tires No. ({tries + 1})")

                audio = Constants.recognizer.listen(source, timeout=Setting.config('time_out'),
                                                    phrase_time_limit=Setting.config('phrase_time_limit'))
            try:
                request = Constants.recognizer.recognize_google(audio, language=Setting.config('lang'))
                Dump.dd(request)
            except Exception as e:
                Dump.dd(e)
                if mode == 'sleeping':
                    return request

                return self.catch(mode, tries)

        except Exception as e:
            Dump.dd(e)
            if mode == 'sleeping':
                return request

            return self.catch(mode, tries)

        return request

    def catch(self, mode, tries):
        if mode == 'normal':
            tries = tries + 1
            if tries < Setting.config('max_listen_try'):
                if tries >= Setting.config('start_waiting_try'):
                    Emoji.change_emoji('waiting')

                return self.listen(tries=tries, with_emoji=False)
            else:
                Dump.dd('Did not get any request, will be sleepy')

    def silent_listening(self, service_process_is_alive):
        try:
            with recognition.Microphone() as source:
                audio = Constants.recognizer.listen(source, timeout=Setting.config('time_out'), phrase_time_limit=5)

            # received audio data, now we'll recognize it using Google Speech Recognition
            try:
                Dump.dd('Try to listen')
                request = Constants.recognizer.recognize_google(audio, language=Setting.config('lang'))
                Dump.dd('got something: ' + request)

                if any(map(request.__contains__,
                           ['اخرس', 'وقف', 'اسكت', 'توقف', 'ستوب', 'اسمع', 'هدي', 'اهدى', 'هلو', 'الو', 'اوقف', 'بس',
                            'خلاص', 'خلص'])):
                    Dump.dd('Terminate current service')
                    service_process_is_alive.value = False
                    Dump.dd('Terminated')
                else:
                    self.silent_listening(service_process_is_alive)

            except Exception as ex:
                Dump.dd('Nothing said')
                Dump.dd(ex)
                self.silent_listening(service_process_is_alive)

        except Exception as ex:
            Dump.dd('Nothing said')
            Dump.dd(ex)
            self.silent_listening(service_process_is_alive)
