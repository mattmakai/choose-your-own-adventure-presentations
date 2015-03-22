from flask.ext.socketio import emit

from . import socketio


@socketio.on('connect', namespace='/cyoa')
def ws_connect():
    pass

@socketio.on('disconnect', namespace='/cyoa')
def ws_disconnect():
    pass

