from __future__ import print_function

from collections import Counter
import struct
import time
import sys
import numpy as np

try:
    import pygame
    from pygame.locals import *
    HAVE_PYGAME = True
except ImportError:
    HAVE_PYGAME = False
import common
import myo_raw
NUMS_OF_SENSORS = 8
NUMS_OF_MOVES = 10
#modelSaved = "Model/modelSaved.yml"
class EMGHandler(object):
    def __init__(self, m):
        self.recording = -1
        self.m = m
        self.emg = (0,) * NUMS_OF_SENSORS
        #self.training = False
    def __call__(self, emg, moving):
        self.emg = emg
        if self.recording >= 0:
            self.m.cls.store_data(self.recording, emg)
        """
        if self.training == True:
            self.m.cls.read_data()
            self.training = False
            print ('Training Complete!')
        """
while  True:
    if __name__ == '__main__':
        if HAVE_PYGAME:
            pygame.init()
            w, h = 1000, 420
            scr = pygame.display.set_mode((w, h))
            font = pygame.font.Font(None, 30)

        m = myo_raw.MyoRaw(myo_raw.RFClassifier(), sys.argv[1] if len(sys.argv) >= 2 else None)
        hnd = EMGHandler(m)
        m.add_emg_handler(hnd)
        m.connect()

        try:
            while True:

                m.run()

                r = m.history_cnt.most_common(1)[0][0]

                if HAVE_PYGAME:
                    for ev in pygame.event.get():
                        if ev.type == QUIT or (ev.type == KEYDOWN and ev.unicode == 'q'):
                            raise KeyboardInterrupt()
                        elif ev.type == KEYDOWN:
                            if K_0 <= ev.key <= K_9:
                                hnd.recording = ev.key - K_0
                            elif K_KP0 <= ev.key <= K_KP9:
                                hnd.recording = ev.key - K_KP0
                            elif K_F1 <= ev.key <= K_F6:
                                hnd.recording = ev.key - K_F1 + 10
                            elif ev.key == K_F7:
                                hnd.saving = True
                            elif ev.key == K_F8:
                                hnd.training = True
                            elif ev.unicode == 'r':
                                hnd.cl.read_data()
                        elif ev.type == KEYUP:
                            if K_0 <= ev.key <= K_9 or K_KP0 <= ev.key <= K_KP9 or K_F1 <= ev.key <= K_F6 :
                                hnd.recording = -1

                    scr.fill((0, 0, 0), (0, 0, w, h))

                    for i in range(NUMS_OF_MOVES):
                        x = 0
                        y = 0 + 32 * i

                        clr = (0,200,0) if i == r else (255,255,255)

                        txt = font.render('%5d' % (m.cls.Y == i).sum(), True, (255,255,255))
                        scr.blit(txt, (x + 20, y))

                        txt = font.render('%d' % i, True, clr)
                        scr.blit(txt, (x + 110, y))


                        scr.fill((0,0,0), (x+130, y + txt.get_height() / 2 - 10, len(m.history) * 20, 20))
                        scr.fill(clr, (x+130, y + txt.get_height() / 2 - 10, m.history_cnt[i] * 20, 20))

                    pygame.display.flip()
                else:
                    print(chr(27) + "[2J")
                    for i in range(NUMS_OF_MOVES):
                        print(i, ' -' * m.history_cnt[i])
                    print('prediction: ', r)
                    print()

        except KeyboardInterrupt:
            pass
        finally:
            m.disconnect()
            print()

        if HAVE_PYGAME:
            pygame.quit()
