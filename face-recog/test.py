#https://github.com/ageitgey/face_recognition

import face_recognition
import cv2
import struct
import time
import csv
import os
import yaml

class Accounts():
    def __init__(self):
        self.users = {}

    def addUser(self, name):
        self.users[name] = [None, None]

    def addPlaylist(self, name, playlist):
        self.users[name][0] = playlist

    def addImg(self, name, imgEnc):
        self.users[name][1] = imgEnc

    def getPlaylist(self, name):
        return self.users[name][0]

    def getImg(self, name):
        return self.users[name][1]

def startVideo():
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    accounts = Accounts()
    image_encodings = []
    account_list = []


    # learn how to recognize faces
    for file in os.listdir('./faces'):
        if file.endswith(".jpg"):
            print file
            name = file.split(".")[0]
            temp_img = face_recognition.load_image_file('./faces/' + str(file))
            temp_encoding = face_recognition.face_encodings(temp_img)[0]
            accounts.addUser(name)
            accounts.addImg(name, temp_encoding)
            account_list.append(name)
            image_encodings.append(temp_encoding)

    # add playlists to user
    with open('playlists.yml', 'r') as file:
        playlists = yaml.load(file)
        for user in playlists:
            print user, playlists[user]
            accounts.addPlaylist(user, playlists[user])
            #accounts.users[user] = playlists[user]

    recognized = False
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        name = "Unknown"
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            match = face_recognition.compare_faces(image_encodings, face_encoding)
            for i in range(len(match)):
                if match[i]:
                    recognized = True
                    name = account_list[i]
                    print name, accounts.getPlaylist(name)
                    ######
                    # CALL PLAYLIST STUFF HERE
                    ######
                    return (name, accounts.getPlaylist(name))


            # Draw a box around the face
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # # Draw a label with a name below the face
            # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if (cv2.waitKey(1) & 0xFF == ord('q')) or recognized:
            time.sleep(1)
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

name, playlist = (startVideo())
print "USER: {}, PLAYLIST: {}".format(name, playlist)
