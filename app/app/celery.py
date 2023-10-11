from celery import Celery
from celery.schedules import crontab

app = Celery('birthday_reminders')  # Use 'Celery' directly, not 'celery.Celery'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-birthday-emails': {
        'task': 'send_birthday_emails.send_emails',
        'schedule': crontab(hour=10, minute=30),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
