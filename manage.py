#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

import os

from cyoa import app, redis_db, socketio
from flask.ext.script import Manager, Shell

manager = Manager(app)

def make_shell_context():
    return dict(app=app, redis_db=redis_db)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def runserver():
    socketio.run(app, "0.0.0.0", port=5001)

if __name__ == '__main__':
    manager.run()
