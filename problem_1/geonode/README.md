### problem
1. Create a celery task on Django Project to scrape
ip,port,protocol,country,and uptime save it into sqlite using MVP Django
then set up a celery schedule to run this task every day.

### environment
Python 3.10.12

### commands in different terminal
- `python manage.py runserver`
- `celery -A geonode worker -l INFO`
- `celery -A geonode beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`

