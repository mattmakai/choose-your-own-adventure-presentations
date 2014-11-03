from flask import Flask
from flask.ext.socketio import SocketIO
import redis

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

from config import REDIS_SERVER, REDIS_PORT, REDIS_DB

redis_db = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)

socketio = SocketIO(app)

from . import views
from . import websockets
