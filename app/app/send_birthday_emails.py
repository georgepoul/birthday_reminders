"""
Asynchronous task for sending birthday emails
"""
from app.app.celery import shared_task
from django.core.mail import send_mail
from datetime import date
from core.models import Birthday

@shared_task
def send_emails():
    today = date.today()
    birthdays_today = Birthday.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)

    for birthday in birthdays_today:
        send_mail(
            'Happy Birthday!',
            'Dear {},\n\nHappy birthday! 🎉'.format(birthday.name),
            [birthday.user.email],
            [birthday.email],
            fail_silently=False,
        )