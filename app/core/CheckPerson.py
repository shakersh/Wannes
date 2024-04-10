from app.core import Constants
from app.core.Image import Image
from app.util.Dump import Dump
from app.util.Translate import Translate
from app.core.Capture import Capture


class CheckPerson:
    def check_person(self):
        Dump.dd("Check person if exist or not")
        Constants.audio.speak(Translate.__('checking_msg'))
        Constants.audio.speak(Translate.__('cheese_msg'))
        if 'تشيز' in Constants.audio.listen():
            new_photo = Capture.handle()
            if Image.person_exist(new_photo):
                Constants.audio.speak(Translate.__('found_person_msg'))
            else:
                Constants.audio.speak(Translate.__('not_found_person_msg'))
