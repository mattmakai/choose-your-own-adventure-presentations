from flask.ext.socketio import emit

from . import socketio


@socketio.on('connect', namespace='/cyoa')
def test_connect():
    pass

@socketio.on('disconnect', namespace='/cyoa')
def test_disconnect():
    pass


@socketio.on('my event', namespace='/cyoa')
def update_count(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})
