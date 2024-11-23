from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
app = Celery("library")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate-admin-report-every-hour": {
        "task": "notifications.task.generate_admin_report",
        "schedule": crontab(minute=0, hour="*"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
