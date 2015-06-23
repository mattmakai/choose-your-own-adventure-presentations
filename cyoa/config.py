import os
from datetime import timedelta

# General Flask app settings
DEBUG = os.environ.get('DEBUG', None)
SECRET_KEY = os.environ.get('SECRET_KEY', None)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)

# Redis connection
REDIS_SERVER = os.environ.get('REDIS_SERVER', None)
REDIS_PORT = os.environ.get('REDIS_PORT', None)
REDIS_DB = os.environ.get('REDIS_DB', None)

# Twilio API credentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_IMPORTS=("cyoa.tasks",)
CELERYBEAT_SCHEDULE = {
    'persist-votes': {
        'task': 'cyoa.tasks.persist_votes',
        'schedule': timedelta(minutes=5),
    }
}
