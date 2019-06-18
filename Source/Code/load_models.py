import common
import utils
import myo_raw

class EMGHandler(object):
    def __init__(self, m):
        self.recording = -1
        self.m = m
        self.emg = (0) * common.NUM_OF_SENSORS
    def __call__(self, emg, moving):
        self.emg = emg
        # print(emg)
        if self.recording >= 0:
            self.m.cls.store_data(self.recording, emg)

def setup():
    m = myo_raw.MyoRaw(myo_raw.RFClassifier(), None)
    hnd = EMGHandler(m)
    m.add_emg_handler(hnd)
    m.connect()
    return (m, hnd)

def runPrediction(m, isRest, preRest, count, moving):
    m.run()
    movingTemp = m.history_cnt.most_common(1)[0][0]

    if (movingTemp == 0):
        isRest = True
    else:
        isRest = False

    if (preRest == True and isRest == False):
        count = 0
    elif (preRest == False and isRest == True):
        count = 0
    else:
        # do current grip (m.last_pose)
        if (count >= 0):
            count += 1
        if (count == 2):
            moving = m.history_cnt.most_common(1)[0][0]
            count = -1

    preRest = isRest
    # print('Prediction: ', common.NAME_OF_MOVE[int(moving)], 'isRest: ', isRest)
    return (isRest, preRest, count, moving)
