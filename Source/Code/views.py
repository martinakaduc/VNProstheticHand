import json
import common
from aiohttp import web, WSMsgType
from aiohttp_session import get_session
import aiohttp_jinja2
from time import time
from datetime import datetime
from settings import log

def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)

def set_session(session, user_data):
    session['user'] = user_data
    session['last_visit'] = time()

def convert_json(message):
    return json.dumps({'error': message})

class MainPage(web.View):
    @aiohttp_jinja2.template('webPage/mainPage.html')
    async def get(self):
        session_user = await get_session(self.request)
        if session_user.get('user'):
            return {'user': session_user.get('user').get('username'),'alert':''}
        else:
            return {'user': '','alert':''}
