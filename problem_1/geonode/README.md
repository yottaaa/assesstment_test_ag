### problem
1. Create a celery task on Django Project to scrape
ip,port,protocol,country,and uptime save it into sqlite using MVP Django
then set up a celery schedule to run this task every day.

### environment
Python 3.10.12

### instructions
1. Build the app `docker compose up -d --build`.
2. Create superuser account `docker compose run --rm django python manage.py createsuperuser`.
3. Go to `localhost:8080` to start scraping or `localhost:8080/schedule` to trigger the scheduling task.
4. You can also change the time or day you want to schedule in the code just go to `scraper/views.py` or add periodic time in admin panel.

