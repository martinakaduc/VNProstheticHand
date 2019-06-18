NUM_OF_SENSORS = 8
NUM_OF_MOVES = 15
SUBSAMPLES = 3
K = 5
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
        [0, 0, 1, 1]]#gun
# NAME_OF_MOVES = ['rest', 'fist', ' plam', 'point', 'pinch', 'tripod', 'hello', 'three', 'four', 'gun', 'promi']
BUTTON_PIN = 7
HIST_LEN = 35
NUMS_OF_EACH_TRAINING = 100
MAX_TRAINING_TIMES = 3 #Each grip
MODEL_FILE = "mainModel.sav"
EMG_DATA_DIR = "../emgData/"
MODEL_DIR = "../Models/"
WEB_STATIC_DIR = "../WebUI/static/"
WEB_MEDIA_DIR = "../WebUI/media/"
WEB_TEMPLATE_DIR = "../WebUI/templates/"
