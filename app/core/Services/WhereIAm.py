from app.core import Constants
from app.core.Emoji import Emoji
from app.util.Dump import Dump
from app.core.Services.Service import Service
from app.util.Translate import Translate
import cv2
from app.core.Move import Move
from app.util.Setting import Setting
from app.util.Helper import Helper

if Helper.is_raspberry():
    from picamera2 import Picamera2
    from tflite_support.task import core
    from tflite_support.task import processor
    from tflite_support.task import vision


class WhereIAm(Service):
    keywords = ['وين انت', 'وين انا']

    def handle(self, request):
        if not Helper.is_raspberry():
            Dump.dd('Platform not supported')
            Constants.audio.speak(Translate.__('not_supported'))
            return

        count = 0
        model = 'resources/efficientdet_lite0.tflite'
        num_threads = 4
        dispW = 480
        dispH = 360
        Dump.dd('Search where I am')
        Constants.audio.speak(Translate.__('where_I_am'))

        Emoji.change_emoji('where')
        piCam = Picamera2()
        piCam.preview_configuration.main.size = (dispW, dispH)
        piCam.preview_configuration.main.format = 'RGB888'
        piCam.preview_configuration.align()
        piCam.configure("preview")
        piCam.start()
        cam = cv2.VideoCapture()
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
        cam.set(cv2.CAP_PROP_FPS, 30)

        found = []
        base_options = core.BaseOptions(file_name=model, use_coral=False, num_threads=num_threads)
        detection_options = processor.DetectionOptions(max_results=4, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
        detector = vision.ObjectDetector.create_from_options(options)
        move = Move()
        while count < 50:
            im = piCam.capture_array()
            imRGB = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            imTensor = vision.TensorImage.create_from_array(imRGB)
            detect = detector.detect(imTensor)
            for detec in detect.detections:
                found.append(detec.categories[0].category_name)

            if Setting.config('debug'):
                cv2.imshow('camera', im)

            if cv2.waitKey(1) == ord('q'):
                break

            found = list(set(found))
            Dump.dd(found)
            move.looking(0.2)
            count += 1

        cv2.destroyAllWindows()
        piCam.stop()
        piCam.__del__()

        move.stop()
        move.clear()
        if ('couch' or 'tv' or 'desk' or 'dining table' or 'chair' or 'clock' or 'vase') in found:
            Constants.audio.speak(Translate.__('in_salon'))

        elif ('toilet' or 'toothbrush' or 'sink' or 'scissors' or 'hair drier' or 'hair brush') in found:
            Constants.audio.speak(Translate.__('in_bathroom'))

        elif ('bed' or 'mirror' or 'teddy bear') in found:
            Constants.audio.speak(Translate.__('in_bedroom'))

        elif (
                'plate' or 'wine glass' or 'fork' or 'knife' or 'spoon' or 'bowl' or 'microwave' or 'oven' or 'toaster' or 'refrigerator' or 'blender') in found:
            Constants.audio.speak(Translate.__('in_kitchen'))

        else:
            Constants.audio.speak(Translate.__('place_not_found'))

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
