from sqlalchemy import or_

from .models import Decision
from . import app, db, redis_db, celery


@celery.task
def persist_votes():
    # assumes votes are saved in a separate redis database
    for key in redis_db.keys():
        try:
            decisions = Decision.query.filter_by(or_(first_path_slug=key,
                                                    second_path_slug=key))
            decisions.first().votes = redis_db.get(key)
            db.session.merge(decision)
        except:
            pass # meh, decision must not be in database
        finally:
            db.session.commit()
