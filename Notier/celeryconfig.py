BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = True
 
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
# CELERY_BEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'



