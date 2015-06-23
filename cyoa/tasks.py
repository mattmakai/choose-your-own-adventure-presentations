from .models import Decision
from . import app, db, redis_db, celery


@celery.task
def persist_votes():
    redis_db.incr('task')
