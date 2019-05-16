from __future__ import print_function
#!/usr/bin/python
import os
#import wiringpi
import common
import load_models
from web_config import webConfig
#wiringpi.wiringPiSetup()
#wiringpi.pinMode(BUTTON_PIN,0)

if __name__ == '__main__':
    if (not os.path.exists(common.MODEL_DIR + common.MODEL_FILE)):
        webConfig()

    # HAVE_DATA = True
    # for i in range(common.NUM_OF_MOVES):
    #     if (not os.path.exists(common.EMG_DATA_DIR + 'vals%s.dat' % i)):
    #         HAVE_DATA = False
    #         break
    # if (not HAVE_DATA):
    #     webConfig()

    (m, hnd) = load_models.setup()
    moving = 0
    isRest = True
    preRest = True
    count = -1

    while True:
        (isRest, preRest, count, moving) = load_models.runPrediction(m, isRest, preRest, count, moving)

    m.disconnect()
