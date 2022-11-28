import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver.settings')

app = Celery('webserver')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'main.tasks.LSI_analize',
        'schedule': crontab(minute='*/15'),
    },
}