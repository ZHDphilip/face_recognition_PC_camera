######
# -*- coding: utf-8 -*-
# © 09/13/2020 by @zihaoDONG. ALL RIGHTS RESERVED
# File: face_recognition_cam.py
######

import cv2
import face_recognition
import numpy as np
import xlsxwriter
import time
from utils import load_data
from utils import getName
from utils import addNewPerson

known_face_encodings = []
known_face_names = []


def update(encoding, name):
    global known_face_encodings, known_face_names
    known_face_encodings.append(encoding)
    known_face_names.append(name)


def dealWithUnknownPerson(frame, face_encoding, top, left, bottom, right):
    cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 255, 0), 3)
    cv2.imshow("Live Camera", frame)
    name = getName()
    addNewPerson(name, face_encoding.tolist())
    update(face_encoding, name)
    if cv2.waitKey(1) == 13:
        return name


def func():
    capture = cv2.VideoCapture(0)
    # in order to make things fast, we process every other frame
    face_locs = []
    face_encodings = []
    face_names = []
    processThisFrame = True
    indi = 0

    while True:
        # read a frame from the camera
        ret, frame = capture.read()
        # Resize the frame so face recognition will be faster
        smallFrame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
        # Convert from BGR to RGB
        smallFrameRGB = smallFrame[:, :, ::-1]

        if processThisFrame:
            # find all faces and encode them
            face_locs = face_recognition.face_locations(smallFrameRGB)
            face_encodings = face_recognition.face_encodings(smallFrameRGB, face_locs)
            face_names = []
            for face_loc, face_encoding in zip(face_locs, face_encodings):
                # check if the face already exists in our database
                # print(known_face_encodings)
                name = "Unknown"
                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.6)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match = np.argmin(face_distances)
                    if matches[best_match]:
                        name = known_face_names[best_match]
                    if name == "Unknown":
                        top, right, bottom, left = face_loc
                        name = dealWithUnknownPerson(frame, face_encoding, top*4, left*4, bottom*4, right*4)
                else:
                    top, right, bottom, left = face_loc
                    name = dealWithUnknownPerson(frame, face_encoding, top * 4, left * 4, bottom * 4, right * 4)
                face_names.append(name)
        processThisFrame = not processThisFrame

        for (top, right, bottom, left), name in zip(face_locs, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # draw box around faces
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)
            # draw label with name below faces
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # display
        cv2.imshow("Live Camera", frame)

        # press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release control
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    known_face_encodings, known_face_names = load_data()
    func()


# import dlib
# import face_recognition
# import cv2
#
# def plot_rectangle(image, faces):
#     for face in faces:
#         cv2.rectangle(image,(face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 3)
#     return image
#
# def main():
#     # read from camera
#     capture = cv2.VideoCapture(0)
#     # if capturn.isOpened() is False:
#     #     print("Camera Error")
#     # See if Camera successfully opened
#     if capture.isOpened():
#         # iteratively get every frame
#         while True:
#             ret, frame = capture.read()
#             if ret:
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 small_gray = cv2.resize(gray, (0, 0), fx = 0.25, fy = 0.25)
#                 # Use Dlib to detect faces
#                 detector = dlib.get_frontal_face_detector()
#                 res = detector(small_gray, 1)
#                 # plot rectangle
#                 processedFrame = plot_rectangle(frame, res)
#                 # display
#                 cv2.imshow("Face Detection", processedFrame)
#                 if cv2.waitKey(1) == 27: # if press ESC, then Abort
#                     break
#         capture.release()
#         cv2.destroyAllWindows()
#     else:
#         print("Failed to open the camera...")
#
#
# if __name__ == '__main__':
#     main()
#
#
# cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 3)
# cv2.imshow("Live Camera", frame)
# if cv2.waitKey(1) == 13:
#     continue
# name = getName()
# addNewPerson(name, face_encoding.tolist())
# update(face_encoding, name)
