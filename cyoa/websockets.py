from flask.ext.socketio import emit

from . import socketio


@socketio.on('connect', namespace='/cyoa')
def test_connect():
    pass

@socketio.on('disconnect', namespace='/cyoa')
def test_disconnect():
    pass

