from __future__ import print_function
#!/usr/bin/python
from collections import Counter
import struct
import time
import sys
import os.path
import shutil
import numpy as np
import os
try:
    import mraa
except ImportError:
    print('Please install or update mraa library!')
try:
    from sklearn import neighbors, svm
    HAVE_SK = True
except ImportError:
    HAVE_SK = False
    print('You do not have sklearn! Casual calculator will be used instead.')
import common
import myo_raw
#import servo

NUM_OF_SENSORS = 8
NUM_OF_MOVES = 11
MOVE_OF_FINGER =[
        [0, 0, 0, 0],#rest
        [1, 1, 1, 1],#fist
        [0, 1, 1, 1],#plam
        [1, 0, 1, 1],#point
        [1, 1, 0, 0],#pinch
        [1, 1, 1, 0],#tripod
        [1, 0, 0, 1],#hello
        [0, 0, 0, 1],#three
        [1, 0, 0, 0],#four
        [0, 0, 1, 1],#gun
NAME_OF_MOVE = ['rest', 'fist', ' plam', 'point', 'pinch', 'tripod', 'hello',
                'three', 'four', 'gun']
NUM_OF_SERVOS = 4
SERVO_PINS = [0, 14, 20, 21]
BUTTON_PIN = 15
HAVE_DATA = False

handServo = [None]*NUM_OF_SERVOS
#Attach servos and do the rest
'''
for i in range(NUM_OF_SERVOS):
    handServo[i] = servo.Servo("%d" % i)
    handServo[i].attach(SERVO_PINS[i])
    handServo[i].write(0)
'''
for i in range(NUM_OF_SERVOS):
    handServo[i] = mraa.Gpio(SERVO_PINS[i])
    handServo[i].dir(mraa.DIR_OUT)
    handServo[i].write(0)

button = mraa.Gpio(BUTTON_PIN)
button.dir(mraa.DIR_IN)

while (HAVE_DATA == False):
    for i in range(NUM_OF_MOVES):
        if (os.path.exists('/mnt/storage/vals%d.dat' % i)):
            os.remove('/root/VNProstheticHand/vals%d.dat' % i)
            shutil.move('/mnt/storage/vals%d.dat' % i, '/root/VNProstheticHand/')
        else:
            HAVE_DATA = False
            time.sleep(1)
            break
        HAVE_DATA = True
    for i in range(NUM_OF_MOVES):
        if (os.path.exists('/root/VNProstheticHand/vals%d.dat' % i)):
            pass
        else:
            HAVE_DATA = False
            print('Please copy recorded data to Edison storage!')
            break
        HAVE_DATA = True

class EMGHandler(object):
    def __init__(self, m):
        self.recording = -1
        self.m = m
        self.emg = (0,) * NUM_OF_SENSORS

    def __call__(self, emg, moving):
        self.emg = emg
        if self.recording >= 0:
            self.m.cls.store_data(self.recording, emg)

while  True:
    if __name__ == '__main__':
        m = myo_raw.MyoRaw(myo_raw.RFClassifier(), sys.argv[1] if len(sys.argv) >= 2 else None)
        hnd = EMGHandler(m)
        m.add_emg_handler(hnd)
        m.connect()
        isRest = True
        preRest = True

        try:
            while True:
                if button.read() == 1:
                    while button.read() == 1:
                        pass
                    break
                m.run()
                moving = m.history_cnt.most_common(1)[0][0]
                if (moving == 0):
                    isRest = True
                else:
                    isRest = False

                if (preRest == True and isRest == False):
                    #do the moving
                    #if hand is not rest, do not do any moving
                    for i in range(NUM_OF_SERVOS):
                        handServo[i].write(MOVE_OF_FINGER[int(moving)][i])
                        #time.sleep(0.005)
                    #print('rest to moving')

                elif (preRest == True and isRest == True):
                    #do the 0 moving if hand is moving to rest
                    for i in range(NUM_OF_SERVOS):
                        handServo[i].write(0)
                        #time.sleep(0.005)
                    #print('moving -> rest')

                preRest = isRest
                print('Prediction: ', NAME_OF_MOVE[int(moving)], 'isRest: ', isRest)
                #time.sleep(0.05)

        except KeyboardInterrupt:
            pass
        finally:
            m.disconnect()
            print()
