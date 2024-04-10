import os
from app.core import Constants
from app.core.Emoji import Emoji
from app.core.Image import Image
from app.util.Dump import Dump
from app.core.Services.Service import Service
from app.core.Capture import Capture
from app.util.Helper import Helper
from app.util.Setting import Setting
from app.util.Translate import Translate


class CheckPerson(Service):
    keywords = ['مين انا', 'بتعرفني', 'عارفني', 'عرفني']

    def handle(self, request):
        Dump.dd('check person')

        while True:
            Constants.audio.speak(Translate.__('check_person'))
            file_name = Helper.generate_name('jpg')
            file = Capture.handle('storage/tmp/' + file_name)

            # Analyze the picture
            # If everything is okay, then break
            # make sure there is only one face first
            # then make sure this face is not exist
            # else => remove the image, and do the process again
            try:
                Emoji.change_emoji('loading')
                image = Image()
                # if not image.has_one_face(file):
                #     Constants.audio.speak(Translate.__('photo_should_has_one_face'))
                # else:
                name = image.get_person(file)

                if not name:
                    Constants.audio.speak(Translate.__('person_not_found'))
                else:
                    Constants.audio.speak(Translate.__('person_found', {"name": name}))

                os.remove(file)
                break
            except:
                Constants.audio.speak(Translate.__('photo_is_not_clear'))

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
