import cv2
from app.util.Helper import Helper

if Helper.is_raspberry():
    from picamera2 import Picamera2


class Capture:

    @staticmethod
    def handle(file=None):
        piCam = Picamera2()
        piCam.preview_configuration.main.size = (1280, 720)
        piCam.preview_configuration.main.format = "RGB888"
        piCam.preview_configuration.align()
        piCam.configure("preview")
        piCam.start()
        screen = 'Main'
        cv2.namedWindow(screen, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(screen, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        delay_seconds = 2

        for _ in range(int(delay_seconds * 10)):
            frame = piCam.capture_array()
            cv2.imshow(screen, frame)

            cv2.waitKey(100)

        piCam.stop()
        piCam.__del__()

        if file is None:
            file = Helper.generate_name('jpg')
        cv2.imwrite(file, frame)
        cv2.destroyAllWindows()

        return file
