################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import time

import sys
# sys.path.append('../../../')
# import test.py

import face_recognition
import cv2
import struct
import time
import csv
import os
import yaml

# from test import startVideo

import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import random

factor = 10

from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type

device = soundtouch_device('192.168.1.157')
device.power_on()
# device.play_media(Source.INTERNET_RADIO, '4712')


trigger = 0


def set_playlist(arg):
    x = arg
    global play
    play = x
    return (play)


# count = 0

# def up_count():
#     x = count
#     global count
#     count= x+1
#     return(count)
#
# def down_count():
#     x = count
#     global count
#     count= x-1
#     return(count)

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        preset = False

        print "gestures: %d" % (len(frame.gestures()))
        # print count

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]


            pinch = hand.pinch_strength
            if(hand.grab_strength == 1 and pinch == 1):
                if(hand.is_right):
                    if(device.status().play_status == "PLAY_STATE"):
                        device.pause()
                    else:
                        device.play()
                if(hand.is_left):
                    weather = get_weather()
                    if(weather == 'Sunny'):
                        device.play_media(Source.SPOTIFY, "spotify:user:popsugarsmart:playlist:1e82JSBwrnZF8TODtUcHeR", "dchen319")
                    else:
                        device.play_media(Source.SPOTIFY, "spotify:user:popsugarsmart:playlist:1vRYaCYXyJCiRWsLcoR88p", "dchen319")


            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
                # print "Hand has %d fingers, average finger tip position: %s" % (
                #       len(fingers), avg_pos)

            # Get the hand's sphere radius and palm position
            # print "Hand sphere radius: %f mm, palm position: %s" % (
            #       hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            # print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" %
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
            #     direction.yaw * Leap.RAD_TO_DEG)

            # Gestures
            for gesture in frame.gestures():

                gest_hands = gesture.hands
                left = gest_hands.leftmost

                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                        rand = random.randrange(start=0, stop=factor, step=1)
                        if(rand == 0):
                            # up_count()
                            device.volume_up()
                        else:
                            continue
                        # up_count()
                        # device.set_volume(50)

                    else:
                        clockwiseness = "counterclockwise"
                        rand = random.randrange(start=0, stop=factor, step=1)
                        if(rand == 0):
                            # down_count()
                            device.volume_down()
                        else:
                            continue
                        # down_count()
                        # device.set_volume(0)

                    # Calculate the angle swept since the last frame
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                    # print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                    #         gesture.id, self.state_string(gesture.state),
                    #         circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
                    print clockwiseness

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    # print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                    #         gesture.id, self.state_string(gesture.state),
                    #         swipe.position, swipe.direction, swipe.speed)


                    rand = random.randrange(start=0, stop=factor/7, step=1)
                    if(swipe.direction[0] < -0.85 and rand == 0 and left.is_right):
                        print("Left")
                        device.previous_track()
                        device.previous_track()
                    if(swipe.direction[0] > 0.85 and rand == 0 and left.is_right):
                        print("Right")
                        device.next_track()

                    if(swipe.direction[0] < -0.85 and rand == 0 and left.is_left):

                        curr = device.status().source
                        if(curr == "INTERNET_RADIO"):
                            device.play_media(Source.LOCAL_MUSIC, "album:4", "b8750a46-7b1e-44a1-bae9-9e896b680b2c", Type.ALBUM)
                        if(curr == "SPOTIFY"):
                            device.play_media(Source.INTERNET_RADIO, "4712")
                        if(curr == "LOCAL_MUSIC"):
                            device.play_media(Source.SPOTIFY, play, "dchen319")
                        if(curr == "INVALID_SOURCE"):
                            device.play_media(Source.INTERNET_RADIO, "4712")

                    if(swipe.direction[0] > 0.85 and rand == 0 and left.is_left):
                        # exit()
                        curr = device.status().source
                        if(curr == "INTERNET_RADIO"):
                            device.play_media(Source.SPOTIFY, play, "dchen319")
                        if(curr == "SPOTIFY"):
                            device.play_media(Source.LOCAL_MUSIC, "album:4", "b8750a46-7b1e-44a1-bae9-9e896b680b2c", Type.ALBUM)
                        if(curr == "LOCAL_MUSIC"):
                            device.play_media(Source.INTERNET_RADIO, "4712")
                        if(curr == "INVALID_SOURCE"):
                            device.play_media(Source.INTERNET_RADIO, "4712")



                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    # print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                    #         gesture.id, self.state_string(gesture.state),
                    #         keytap.position, keytap.direction )


                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    screentap = ScreenTapGesture(gesture)
                    # print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
                    #         gesture.id, self.state_string(gesture.state),
                    #         screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"




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
                    device.play_media(Source.SPOTIFY, accounts.getPlaylist(name), "dchen319")
                    return (name, accounts.getPlaylist(name))


        # Hit 'q' on the keyboard to quit!
        if (cv2.waitKey(1) & 0xFF == ord('q')) or recognized:
            time.sleep(1)
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

import requests
import yaml
import json

#import face.face_recog as test

#wunderground API
def get_weather():

    with open('creds.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['wunderground']
    url = 'http://api.wunderground.com/api/{}/hourly/forecast/q/NY/NewYork.json'.format(key)
    r = requests.get(url)

    json_string = r.text
    parsed_json = json.loads(json_string)

    forecast_prefix = parsed_json['forecast']['txt_forecast']['forecastday'][2]
    forecast = str(forecast_prefix['fcttext_metric']).split(".")
    forecast_msg = (forecast)
    return forecast_msg[0]


def main():

    import subprocess
    subprocess.Popen([r"Visualizer.exe"])

    # Create a sample listener and controller
    name, playlist = (startVideo())
    print "USER: {}, PLAYLIST: {}".format(name, playlist)

    set_playlist(playlist)

    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
