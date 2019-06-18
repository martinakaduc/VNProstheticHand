import numpy as np
import asyncio
import socketio
import pickle
import jinja2
import base64
from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2 as jtemplate
from routes import routes
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
import os
import common
import load_models

currentGrip = -1
moving = 0
prediction = list(np.zeros(common.NUM_OF_MOVES))
(m, hnd) = load_models.setup()

sio = socketio.AsyncServer(async_mode='aiohttp')
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
app = web.Application(
    middlewares=[
        session_middleware(EncryptedCookieStorage(secret_key)),
    ]
)
sio.attach(app)

#webConfig
@sio.on('time elapsed', namespace='/test')
async def time_elapsed():
  """Example of how to send server generated events to clients."""
  second = 0
  minute = 0
  hour = 0
  while True:
      await sio.sleep(1)
      second += 1
      if second == 60:
          second = 0
          minute += 1
          if minute == 60:
              minute = 0
              hour += 1
      await sio.emit('time elapsed', {'data': '%s : %s : %s' % (hour, minute, second)},
                     namespace='/test')

@sio.on('move data', namespace='/test')
async def push_data():
  global moving
  while True:
      # m.run()
      for i in range(common.NUM_OF_MOVES):
          prediction[i] = round((m.history_cnt[i] / common.HIST_LEN * 100), 0)
      await sio.sleep(0.01)
      await sio.emit('move data', {'data': '%s' % prediction},
                  namespace='/test')
      await sio.emit('grip receive', {'data': '%s' % moving},  namespace='/test')

@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
  await sio.disconnect(sid, namespace='/test')
  # Save Model here
  m.cls.saveModel(common.MODEL_DIR + common.MODEL_FILE)
  # os.system('reboot')

@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
  await sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                 namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
  print('Client disconnected')
"""
0-9 Grip 0-9
10 Start Training Model
"""
@sio.on('button pressed', namespace='/test')
async def button_pressed(sid, gripOrder):
  global currentGrip
  if gripOrder == 'start':
      currentGrip = -1
      gripOrder = -1

  if gripOrder == -1:
      currentGrip += 1
      await sio.emit('train grip', {'data': currentGrip}, room = sid, namespace='/test')
      await sio.emit('my response', {'data': 'Grip %s: %s/%s' % (currentGrip, (int(m.cls.numOfY[currentGrip] / common.NUMS_OF_EACH_TRAINING)), common.MAX_TRAINING_TIMES) }, room = sid, namespace='/test')

  elif isinstance(gripOrder, int):
      print('Training grip ' + str(gripOrder))
      if (int(m.cls.numOfY[gripOrder] / common.NUMS_OF_EACH_TRAINING) < common.MAX_TRAINING_TIMES):

          hnd.recording = gripOrder
          tempY = m.cls.numOfY[gripOrder] + common.NUMS_OF_EACH_TRAINING
          while (m.cls.numOfY[gripOrder] < tempY):
#                    a = datetime.now()
              m.run()
#                    print(datetime.now() - a)
              await sio.emit('my response', {'data': 'Grip %s is training!!!' % gripOrder}, room = sid, namespace='/test')
          hnd.recording = -1
          await sio.emit('my response', {'data': 'Grip %s: %s/%s' % (currentGrip, (int(m.cls.numOfY[currentGrip] / common.NUMS_OF_EACH_TRAINING)), common.MAX_TRAINING_TIMES) }, room = sid, namespace='/test')
      else:
          await sio.emit('my response', {'data': 'Grip %s is full! If you want to retrain, please click [Delete All Data Grip %s] button and try again!' % (gripOrder, gripOrder)}, room = sid, namespace='/test')
      print('trained')

  elif gripOrder[0] == 'D':
      if (os.path.exists(common.EMG_DATA_DIR + 'vals%s.dat' % int(gripOrder[1]))):
          os.remove(common.EMG_DATA_DIR + 'vals%s.dat' % int(gripOrder[1]))
          m.cls.read_data()
          await sio.emit('my response', {'data': 'Grip %s: %s/%s' % (currentGrip, (int(m.cls.numOfY[currentGrip] / common.NUMS_OF_EACH_TRAINING)), common.MAX_TRAINING_TIMES) }, room = sid, namespace='/test')

@sio.on('run emg', namespace='/test')
async def run_emg():
  global moving
  moving = 0
  count = -1
  isRest = True
  preRest = True

  while True:
      (isRest, preRest, count, moving) = load_models.runPrediction(m, isRest, preRest, count, moving)
      await sio.sleep(0.0001)


app['websockets'] = []
app.add_routes(routes)
app.router.add_static('/static', common.WEB_STATIC_DIR, name='static')
app.router.add_static('/media', common.WEB_MEDIA_DIR, name='media')
jtemplate.setup(app, loader=jinja2.FileSystemLoader(common.WEB_TEMPLATE_DIR))

def webConfig():
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(initdb.createdb())
    sio.start_background_task(time_elapsed)
    sio.start_background_task(run_emg)
    sio.start_background_task(push_data)
    web.run_app(app)
    loop.close()
