from django.shortcuts import render
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .tasks import scrape_task

def index(request):
    scrape_task.delay()
    return HttpResponse("Task Started!")

def schedule_task(request):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=2,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="scraping-schedule",
        task="scraper.tasks.scrape_task",
    )

    return HttpResponse("Scraper task scheduled!")