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


class AddPerson(Service):
    keywords = ['ضيف شخص', 'شخص جديد', 'اضافة شخص', 'اضافة حد']

    def handle(self, request):
        Dump.dd('adding new person')
        Constants.audio.speak(Translate.__('add_person'))

        new_name = None
        while new_name is None:
            Constants.audio.speak(Translate.__('add_person_get_name'))
            new_name = Constants.audio.listen()

        while True:
            Constants.audio.speak(Translate.__('add_person_get_photo', {"name": new_name}))

            Emoji.change_emoji('counter')
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
                if not image.has_one_face(file):
                    Constants.audio.speak(Translate.__('photo_should_has_one_face'))
                    os.remove(file)

                elif image.person_exist(file):
                    Constants.audio.speak(Translate.__('person_already_exist'))
                    os.remove(file)

                else:
                    Constants.audio.speak(Translate.__('add_person_success', {"name": new_name}))
                    self.move_file(file, new_name)
                    break
            except:
                Constants.audio.speak(Translate.__('photo_is_not_clear'))

        Constants.audio.speak(Translate.__('need_other_help'))

    def move_file(self, file, new_name, counter=0):
        target_name = new_name
        if counter > 0:
            target_name = new_name + "(" + str(counter) + ")"

        if os.path.exists('storage/photos/' + str(target_name) + '.jpg'):
            self.move_file(file, new_name, counter + 1)
        else:
            os.replace(file, 'storage/photos/' + str(target_name) + '.jpg')

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
