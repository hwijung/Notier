from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings
from datetime import timedelta

# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notier.settings')

app = Celery('Notier', broker='amqp://', backend='amqp://', include=['alarm.tasks'])
# app.config_from_object('django.conf:settings')
app.conf.update(
                BROKER_URL = 'amqp://',
                CELERY_RESULT_BACKEND = 'amqp://',                
                CELERY_TASK_SERIALIZER = 'json',
                CELERY_RESULT_SERIALIZER = 'json',
                CELERY_ACCEPT_CONTENT=['json'],  
                CELERY_TIMEZONE = 'Asia/Seoul',
                CELERY_ENABLE_UTC = True,
                CELERYD_CONCURRENCY = 1,
                CELERYBEAT_SCHEDULE = {
                    'runs-every-minutes': {
                        'task':'alarm.tasks.scrap',
                        'schedule':timedelta(seconds=30)
                        }
# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
# CELERY_BEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'                                       
})

# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
if __name__ == '__main__':
    app.start()
    