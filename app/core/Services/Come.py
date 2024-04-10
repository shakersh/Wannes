from app.core import Constants
from app.core.Move import Move
from app.core.Services.Service import Service
from app.util.Dump import Dump
from app.util.Setting import Setting
from app.util.Helper import Helper
from app.util.Translate import Translate
import cv2

if Helper.is_raspberry():
    from picamera2 import Picamera2


class Come(Service):
    keywords = ['تعال', 'تعالي', 'تعالالي']

    def __init__(self):
        # self.turning = []
        self.is_avoiding = False
        self.move = Move()

    def handle(self, request):
        if not Helper.is_raspberry():
            Dump.dd('Platform not supported')
            Constants.audio.speak(Translate.__('not_supported'))
            return

        piCam = Picamera2()
        piCam.preview_configuration.main.size = (480, 360)
        piCam.preview_configuration.main.format = "RGB888"
        piCam.preview_configuration.align()
        piCam.configure("preview")
        piCam.start()
        face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')

        reach = False
        current_side = 'right'
        trying = 0
        avoid_trying = 0
        last_move = None
        is_face = False

        while not reach and trying < Constants.turn_360:
            Dump.dd('try = ' + str(trying) + ', try_avoiding = ' + str(avoid_trying))
            frame = piCam.capture_array()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frameGray, 1.1, 4)
            Dump.dd(faces)
            if len(faces) == 0:
                if (not self.is_avoiding) or (avoid_trying < 10):
                    Dump.dd('no faces found ..., looking into side: ' + current_side)
                    Dump.dd('is_avoiding: ' + str(self.is_avoiding))

                    self.move.looking(Constants.looking_speed, current_side)
                    last_move = 'looking'
                    if Setting.config('log_driver') == 'sound':
                        self.move.stop()
                    trying += 1
                    avoid_trying += 1
                elif self.is_avoiding:
                    self.is_avoiding = False
                    trying = avoid_trying = 0
                    # TODO: Keep forwarding while blocker still on the left/right side
                    is_avoiding = self.move.forward(2)
                    current_side = self.opposite(current_side)
                    Dump.dd('change side to: ' + (current_side))

            elif is_face:
                is_face = False
                trying = avoid_trying = 0
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    cx = int(x + x + w) // 2
                    cy = int(y + y + h) // 2
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    face_position = int(cx) // 62

                    if (w >= Constants.face_width or h >= Constants.face_height) and self.move.reach():
                        Dump.dd('reached')
                        reach = True
                        break

                    elif self.move.has_block():
                        Dump.dd('blocker found, turning: ' + current_side)
                        current_side = self.avoid(side=current_side)
                        last_move = 'avoid'
                        continue

                    else:
                        self.is_avoiding = False

                    Dump.dd("face_position = " + str(face_position))
                    self.move.curve(face_position, last_move)
                    last_move = 'curve'

                    break
            else:
                is_face = True

            if Setting.config('debug'):
                cv2.imshow('img', frame)

            if cv2.waitKey(30) & 0xff == 27:
                break

        self.move.stop()
        self.move.clear()
        cv2.destroyAllWindows()
        piCam.stop()
        piCam.__del__()

    def avoid(self, side='right'):
        Dump.dd('start avoiding...')
        self.is_avoiding = True

        if side == 'right' and self.move.right_blocker():
            side = 'left'
            if self.move.left_blocker():
                side = 'backward'
        elif side == 'left' and self.move.left_blocker():
            side = 'backward'

        if side == 'right':
            self.move.right(Constants.avoiding_speed)
            if Setting.config('log_driver') == 'sound':
                self.move.stop()
        elif side == 'left':
            self.move.left(Constants.avoiding_speed)

            if Setting.config('log_driver') == 'sound':
                self.move.stop()
        else:
            self.move.backward(0.1, Constants.avoiding_speed)

            if Setting.config('log_driver') == 'sound':
                self.move.stop()

        return side

    @staticmethod
    def opposite(side):
        if side == 'right':
            return 'left'

        return 'right'

    @staticmethod
    def post_action():
        Setting.update('has_welcome', False)
