ps auxww | grep 'celery -A Notier beat' | awk '{print $2}' | xargs kill -9

