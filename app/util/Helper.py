from app.util.Setting import Setting
import random
import string
import platform


class Helper:

    @staticmethod
    def is_raspberry():
        if platform.platform() == 'Linux-6.1.21-v8+-aarch64-with-glibc2.31':
            return True

        return False

    @staticmethod
    def generate_name(extension):
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits,
                           k=Setting.config('file_name_length'))) + '.' + extension

    @staticmethod
    def get_raw_request(request, keywords):
        # first remove any calling style
        constants = ['يا ونيس', 'ونيس']
        keywords = constants + keywords
        for key in keywords:
            request = request.replace(key, '')

        return request

    @staticmethod
    def get_hours(value, lang='ar'):
        if lang == 'ar':
            switcher = {
                0: " الثانية عشر",
                1: " الواحِدَ",
                2: " الثَّانيَ",
                3: " الثَّالِثَ",
                4: " الرَّابِعَ",
                5: " الخامِسَ",
                6: " السَّادِسَ",
                7: " السَّابِعَ",
                8: " الثَّامِنَ",
                9: " التَّاسِعَ",
                10: " العاشِرَ",
                11: " الحاديَتَ عَشَرْ",
                12: " الثَّانِيَتَ عَشَرْ",
            }

        return switcher.get(value)

    @staticmethod
    def get_minutes(value, lang='ar'):
        minutes = ''
        if lang == 'ar':
            if value == 0:
                return ''
            elif value == 1:
                return ' وَدَقِيْقَتٌ واحِدَ '
            elif value == 2:
                return ' وَدَقِيْقَتَيْنِ '
            elif value > 2 and value < 10:
                return " و " + str(value) + " دَقَاَئِقْ "
            else:
                return " و " + str(value) + " دَقِيْقَ "

        return minutes

    @staticmethod
    def get_clock(clock):
        words = clock.split()
        numbers_dict = {
            'وحده': '1',
            'ثنتين': '2',
            'ثلاثه': '3',
            'اربعه': '4',
            'خمسه': '5',
            'سته': '6',
            'سبعه': '7',
            'ثمانيه': '8',
            'تسعه': '9',
            'عشره': '10',
            'وربع': '15',
            'وتلت': '20',
            'ونص': '30',
        }

        # Process each word in the input
        for word in words:
            # Check if the word is in the numbers_dict
            if word in numbers_dict:
                number = str(numbers_dict[word])
                clock = clock.replace(word, number)

        text = clock.replace(':', ' and ')

        res = [int(i) for i in text.split() if i.isdigit()]
        if len(res) == 0:
            hour = 0
        elif len(res) == 1:
            hour = res.pop(0)
            clock = " الساعة " + str(hour) + ":00"
        else:
            hour = res.pop(0)
            clock = " الساعة " + str(hour) + ":" + str(res.pop(0))

        return clock, hour
