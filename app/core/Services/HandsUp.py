from app.core import Constants
from app.core.Emoji import Emoji
from app.core.Services.Service import Service
from app.util.Helper import Helper
from app.util.Setting import Setting
import cv2
import mediapipe as mp
import time
from python_carbon import Carbon
from app.util.Translate import Translate

if Helper.is_raspberry():
    from picamera2 import Picamera2


class HandsUp(Service):
    keywords = ['ارفع يديك', 'ارفع ايديك', 'ارفع ايدك', 'ارفع يدك', 'هقتلك', 'حقتلك', 'راح اقتلك', 'راح ادبحك', 'هدبحك',
                'حدبحك']

    def handle(self, request):
        dispW = 480
        dispH = 360

        if Helper.is_raspberry():
            piCam = Picamera2()
            piCam.preview_configuration.main.size = (dispW, dispH)
            piCam.preview_configuration.main.format = 'RGB888'
            piCam.preview_configuration.align()
            piCam.configure("preview")
            piCam.start()

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
        cap.set(cv2.CAP_PROP_FPS, 30)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mp_draw = mp.solutions.drawing_utils
        end_at = Carbon.now().addSeconds(10)

        Emoji.change_emoji('scare')

        while Carbon.now().lessThan(end_at):
            if Helper.is_raspberry():
                image = piCam.capture_array()
            else:
                success, image = cap.read()

            imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(imageRGB)

            if Setting.config('debug'):
                cv2.imshow('camera', image)

            if cv2.waitKey(1) == ord('q'):
                break

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    hand_landmarks = handLms.landmark

                    if len(hand_landmarks) == 21:  # See all hands points (21 point)
                        for id, lm in enumerate(hand_landmarks):
                            if id == 8:  # id=8 mean we see the finger_tip
                                Emoji.change_emoji('handsup')
                                time.sleep(2)
                                break
                    else:
                        mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

                Constants.audio.speak(Translate.__('happy_to_play_with_you'))

        cap.release()
        cv2.destroyAllWindows()

        if Helper.is_raspberry():
            piCam.stop()
            piCam.__del__()

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
