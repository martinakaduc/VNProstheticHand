from aiohttp import web
from views import MainPage

routes = [
    web.get('/', MainPage, name='mainpage'),
    # web.get('/ws', WebSocket)
]
