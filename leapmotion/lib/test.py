################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################



import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import random

factor = 30

# from libsoundtouch import soundtouch_device
# from libsoundtouch.utils import Source, Type
#
# device = soundtouch_device('192.168.1.157')
# device.power_on()
# device.play_media(Source.INTERNET_RADIO, '4712')


trigger = 0

count = 0

def up_count():
    x = count
    global count
    count= x+1
    return(count)

def down_count():
    x = count
    global count
    count= x-1
    return(count)

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

        print "gestures: %d" % (len(frame.gestures()))
        # print count

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

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
                            up_count()
                        else:
                            continue
                        # up_count()
                        # device.set_volume(50)

                    else:
                        clockwiseness = "counterclockwise"
                        rand = random.randrange(start=0, stop=factor, step=1)
                        if(rand == 0):
                            down_count()
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


                    rand = random.randrange(start=0, stop=factor/4, step=1)
                    if(swipe.direction[0] < -0.8 and rand == 0 and left.is_right):
                        print("Left")
                    if(swipe.direction[0] > 0.8 and rand == 0 and left.is_right):
                        print("Right")
                    if(swipe.direction[0] < -0.8 and rand == 0 and left.is_left):
                        print("Left")
                        exit()
                    if(swipe.direction[0] > 0.8 and rand == 0 and left.is_left):
                        print("Right")
                        exit()




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

def main():
    # Create a sample listener and controller
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
