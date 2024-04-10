from app.core import Constants
from app.core.Emoji import Emoji
from app.core.Services.Service import Service
from app.util.Dump import Dump
from app.util.Helper import Helper
from app.util.Setting import Setting
from app.util.Translate import Translate
from dateutil.parser import parse
from python_carbon import Carbon


class Alarm(Service):
    keywords = ['صحيني', 'نبهني', 'حط منبه', 'حط تذكير', 'ذكرني', 'المنبه', 'منبه']
    frequencies = ['onetime', 'working_days', 'daily']

    def handle(self, request):
        time = ""

        try:
            # day = None
            Constants.audio.speak(Translate.__('alarm_day'))
            day = Constants.audio.listen()
            time = time + " " + day

            Constants.audio.speak(Translate.__('alarm_clock'))
            clock = Constants.audio.listen()
            clock, hour = Helper.get_clock(clock)
            time = time + " " + clock

            if hour <= 12 and hour > 0:
                Constants.audio.speak(Translate.__('alarm_am_pm'))
                am_pm = Constants.audio.listen()
                time = time + " " + am_pm

            time = Translate.google_translate(time, 'en')

            date = Carbon(parse(time, fuzzy=True))
            if date.format('%d') == Carbon.now().format('%d'):
                if day.find('بعد بكره') >= 0:
                    date = date.addDays(2)
                elif day.find('بكره') >= 0:
                    date = date.addDays(1)

            Dump.dd(date.format('%Y-%m-%d %H:%M:%S'))

            cur = Constants.conn.cursor()
            cur.execute(f'INSERT INTO alarms (time) VALUES ("{date.format("%Y-%m-%d %H:%M:%S")}")')
            Constants.conn.commit()

            Constants.audio.speak(Translate.__('alarm_sat'))
        except Exception as e:
            Dump.dd(e)
            Constants.audio.speak(Translate.__('error_while_setting_alarm'))
            self.handle(request)

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)

    @staticmethod
    def run():
        cur = Constants.conn.cursor()
        cur.execute(f'SELECT * FROM alarms WHERE time <= "{Carbon.now().format("%Y-%m-%d %H:%M:%S")}"')
        rows = cur.fetchall()

        if len(rows):
            Emoji.change_emoji('alarm')

            # remove alarm
            cur.execute(f'DELETE FROM alarms WHERE time <= "{Carbon.now().format("%Y-%m-%d %H:%M:%S")}"')
            Constants.conn.commit()
            cur.close()
