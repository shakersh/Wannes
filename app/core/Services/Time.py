from python_carbon import Carbon
from app.core import Constants
from app.core.Services.Service import Service
from app.util.Helper import Helper
from app.util.Setting import Setting
from app.util.Translate import Translate


class Time(Service):
    keywords = ['كم الساعة', 'قديش الساعة', 'اكم الساعة', 'الساعة كم', 'الساعة اكم', 'ايش الساعة', 'كم ساعتك',
                'اكم ساعتك', 'كم الساعه', 'قديش الساعه', 'اكم الساعه', 'الساعه كم', 'الساعه اكم', 'ايش الساعه',
                'كم ساعتك', 'اكم ساعتك']

    def handle(self, request):
        hours = int(Carbon.now().format('%H'))
        minutes = int(Carbon.now().format('%M'))
        a = 'am'

        if hours > 12:
            a = 'pm'

        hours = hours % 12

        phrase = Translate.__('time') + Helper.get_hours(hours) + Helper.get_minutes(minutes) + Translate.__(a)
        Constants.audio.speak(phrase)

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
