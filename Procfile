web: daphne jinxbackend.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=jinxbackend.settings -v2
release: python manage.py migrate