./kill_beat.sh
celery -A Notier beat -f ./celery-log
# celery -A Notier beat -l debug -f ./celery-log
