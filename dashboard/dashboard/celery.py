from __future__ import absolute_import, unicode_literals
import os

from celery.schedules import crontab
from celery import Celery
import logging.config
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE','dashboard.settings')

app = Celery('dashboard')
app.conf.enable_utc = False

app.conf.update(timezone= 'Asia/Kolkata')

# app.config_from_object('django.conf:settings',namespace='CELERY')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send-mail-everyday-at-8':{
#         'task':'send_mail_app.tasks.send_mail_func',
#         'schedule': crontab(hour=12,minute=3),
#         # 'args': ()
#     }
# }

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Configure logging to send logs to stdout
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING)