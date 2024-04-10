from app.core.Emoji import Emoji
from app.core.Services.Service import Service
from app.util.Setting import Setting


class Sleep(Service):
    keywords = ['اخرس', 'نام', 'اصمت', 'تخرس']

    def handle(self, request):
        Setting.update('is_forever_sleep', True)
        return

    @staticmethod
    def pre_action():
        Emoji.change_emoji('sleep')
