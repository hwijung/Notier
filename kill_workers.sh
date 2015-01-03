ps auxww | grep 'celery -A Notier worker' | awk '{print $2}' | xargs kill -9
