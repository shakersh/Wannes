from app.util.Dump import Dump
from app.util.Setting import Setting
from python_carbon import Carbon


class Mode:
    @staticmethod
    def sleepy():
        # Set sleepy mode
        Setting.update('mode', 'sleepy')
        Setting.update('sleepy_time', Carbon.now())

        # TODO: Switch off all unnecessary resources to save battery
        Dump.dd("Entering sleepy mode, No answer till you call me by my name ....")

    @staticmethod
    def sleep():
        # Set sleep mode
        Setting.update('mode', 'sleep')
        Setting.update('is_forever_sleep', False)

        # TODO: Switch off all unnecessary resources to save battery
        Dump.dd("Entering sleep mode, No answer till you call me by my name ....")

    @staticmethod
    def wakeup():
        Setting.update('mode', 'normal')
        Setting.update('sleepy_time', None)
        Setting.update('is_forever_sleep', False)

        # TODO: Switch on all resources again
        Dump.dd('Wakeup ....')

    @staticmethod
    def time_to_sleep():
        if Setting.config('mode') == 'sleep':
            return False

        sleepy_time = Setting.config('sleepy_time')
        if not sleepy_time:
            return False

        sleep_time = sleepy_time.addSeconds(Setting.config('sleep_after'))

        if Carbon.now().greaterThanOrEqualTo(sleep_time):
            return True

        return False
