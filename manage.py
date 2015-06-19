from gevent import monkey
monkey.patch_all()

import os
import redis

from cyoa import app, redis_db, socketio, db
from cyoa.models import Wizard
from flask.ext.script import Manager, Shell

manager = Manager(app)

def make_shell_context():
    return dict(app=app, redis_db=redis_db, db=db, Wizard=Wizard)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def syncdb():
    db.create_all()

@manager.command
def runserver():
    socketio.run(app, "0.0.0.0", port=5001)

@manager.command
def create_wizard(name, password):
    try:
        db.session.add(Wizard(name, password))
        db.session.commit()
    except:
        # user already created. swallow
        pass

@manager.command
def clear_redis():
    redis_cli = redis.StrictRedis(host='localhost', port='6379', db='0')
    redis_cli.delete('done')
    redis_cli.delete('more')
    redis_cli.delete('yes')
    redis_cli.delete('no')

if __name__ == '__main__':
    manager.run()

