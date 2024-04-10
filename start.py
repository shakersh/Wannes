# -*- coding: utf-8 -*-
import time
from app.core import Constants
from app.core.Audio import Audio
import speech_recognition as recognition
import sqlite3
from app.core.Services.Alarm import Alarm
from app.util.Helper import Helper
from migrations.migrations import Migrations

Constants.audio = Audio()

Constants.recognizer = recognition.Recognizer()
with recognition.Microphone() as source:
    Constants.recognizer.adjust_for_ambient_noise(source, duration=3)
    Constants.recognizer.dynamic_energy_threshold = True

Constants.conn = sqlite3.connect('storage/db/robot.db')
Migrations.handle()

if Helper.is_raspberry():
    from gpiozero import LineSensor
    from gpiozero import DistanceSensor
    
    Constants.sensor_up = DistanceSensor(echo=Constants.Echo1, trigger=Constants.Trig1)
    Constants.sensor_right = DistanceSensor(echo=Constants.Echo2, trigger=Constants.Trig2)
    Constants.sensor_down = DistanceSensor(echo=Constants.Echo3, trigger=Constants.Trig3)
    Constants.sensor_left = DistanceSensor(echo=Constants.Echo4, trigger=Constants.Trig4 )
                           
if __name__ == "__main__":
    from app.util.Dump import Dump
    from datetime import datetime

    # Dump.dd("process start at: " + str(datetime.now()))

    from multiprocessing import Process, Array, Value
    from app.core.Emoji import Emoji

    # Booting
    Constants.feeling = Array('c', bytes('booting', "utf-8"))
    emoji = Emoji()
    Constants.emoji_process = Process(target=emoji.booting, args=(Constants.feeling,))
    Constants.emoji_process.start()

    from app.core.Journeys.RegularJourney import RegularJourney
    from app.core.Mode import Mode
    from app.util.Resources import Resources
    from app.util.Setting import Setting


    def main():
        Dump.dd('Initializing System ..')

        # Load all system files for the first run (to not taking time later)
        resource = Resources()
        resource.load()

        Dump.dd("resource loaded at: " + str(datetime.now()))
        # TODO: Check if it's the first time to run or not
        # If not, go with regular_journey
        # for now, we will make it "True" always
        is_regular_journey = True

        # TODO: need to get the stored language for this robot, and set in config
        # for now, we will make it "ar" always
        Setting.update('lang', 'ar')

        while Constants.feeling.value == bytes('booting', "utf-8"):
            time.sleep(0.3)

        Dump.dd('finish branding')
        process = RegularJourney()

        if Helper.is_raspberry():
            head_touch = LineSensor(Constants.TouchHead)
            body_touch = LineSensor(Constants.TouchBody)

        Dump.dd('Defining the process ..')
        while is_regular_journey:
            Dump.dd('Inside the RegularJourney loop ..')

            # Check Alarm
            current_time = time.localtime()
            if current_time.tm_min % 5 == 0:
                Dump.dd('in alarm check')
                Alarm.run()

            # Check Sensors
            if Helper.is_raspberry():
                if head_touch.value:
                    if Setting.config('mode') in ['sleep']:
                        Emoji.change_emoji('nervous')
                    else:
                        Emoji.change_emoji('comfort')

                    time.sleep(1)

                if body_touch.value:
                    if Setting.config('mode') in ['sleep']:
                        Emoji.change_emoji('nervous')
                    else:
                        Emoji.change_emoji('tick')

                    time.sleep(1)

            # Check if the last request is to sleep forever?
            if Setting.config('is_forever_sleep') or Mode.time_to_sleep():
                Dump.dd('Its time to go to sleep, good by')
                Mode.sleep()

            # Go with the process
            if Setting.config('mode') in ['sleep', 'sleepy']:
                Dump.dd('Silent Listening ..')
                Emoji.change_emoji(Setting.config('mode'))
                process.sleep_listening()

            else:
                if Setting.config('has_welcome'):
                    Dump.dd('running the process from the beginning ..')
                    process.welcome()
                    Setting.update('has_welcome', False)

                # listen to take the order
                request = Constants.audio.listen()

                if request:
                    Emoji.change_emoji('search')

                service = process.classify_request(request)

                if service:
                    service.pre_action()

                    if service.is_background_job():
                        silent_listening()
                        Constants.service_process = Process(target=process.handle_request,
                                                            args=(service, request, Constants.feeling))
                        Constants.service_process.start()

                        while Constants.service_process.is_alive() and Constants.service_process_is_alive.value:
                            continue

                        Constants.service_process.terminate()

                        Emoji.change_emoji('listen')

                        Dump.dd('Stop Listening Now....')
                        Constants.service_listen.terminate()
                    else:
                        process.handle_request(service, request, Constants.feeling)

                    service.post_action()

        Dump.dd('Shutting Down ..')


    def silent_listening():
        Dump.dd('start silent listening')
        Constants.service_process_is_alive = Value('i', True)
        Constants.service_listen = Process(target=Constants.audio.silent_listening,
                                           args=(Constants.service_process_is_alive,))
        Constants.service_listen.start()


    # TODO:
    # Convert Translation File to class based
    # Enhance the interactive time in listen function
    # Should have a stop in AddPerson (like cancel)
    # Enhance performance & Carbig 

    main()
