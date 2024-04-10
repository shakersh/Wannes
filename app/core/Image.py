import face_recognition
from app.util.Dump import Dump
import cv2
import os


class Image:
    @staticmethod
    def has_one_face(image):
        image = face_recognition.load_image_file(image)  # open image
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # inverse color
        Dump.dd('Checking faces')
        faces = face_recognition.face_locations(image)
        Dump.dd(faces)
        return len(faces) == 1

    def person_exist(self, image):
        # open all photos inside /storage/photos
        # compare the image parameter with stored photos
        # when found, return True
        # otherwise, return false

        for photo in os.listdir('storage/photos/'):
            if photo.endswith('.jpg'):
                photo = 'storage/photos/' + photo
                result = self.face_detect(image, photo)
                if result:
                    return True

        return False

    def get_person(self, image):
        for photo in os.listdir('storage/photos/'):
            if photo.endswith('.jpg'):
                name = photo.replace('.jpg', '')
                photo = 'storage/photos/' + photo
                result = self.face_detect(image, photo)
                if result:
                    return name

        return False

    @staticmethod
    def face_detect(image1, image2):
        # **************************************
        # load and open for two picture
        # **************************************
        image1 = face_recognition.load_image_file(image1)  # open image
        image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)  # inverse color
        image2 = face_recognition.load_image_file(image2)  # open image
        image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)  # inverse color
        # **************************************
        # Select and pin the face for two picture
        # **************************************
        face1 = face_recognition.face_locations(image1)[0]  # select face location on pic
        encode_face1 = face_recognition.face_encodings(image1)[0]  # encoding face on pic
        cv2.rectangle(image1, (face1[3], face1[0]), (face1[1], face1[2]), (255, 0, 255), 2)
        # draw rectangle around face
        face2 = face_recognition.face_locations(image2)[0]  # select face location on pic
        encode_face2 = face_recognition.face_encodings(image2)[0]  # encoding face on pic
        cv2.rectangle(image2, (face2[3], face2[0]), (face2[1], face2[2]), (255, 0, 255), 2)
        # draw rectangle around face
        # **************************************
        # compare between two picture and get the resualt if it is the same face that will print True
        # **************************************
        results = face_recognition.compare_faces([encode_face1], encode_face2)
        return results[0]
