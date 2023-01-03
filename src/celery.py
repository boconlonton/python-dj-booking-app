import os

import json

import logging

from celery import Celery

from django.core.mail import send_mail
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('booking_worker')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_confirmation_email(self, booking):
    data = json.loads(booking)
    data = data[0].get('fields')
    send_mail('[no-reply] Booking Confirmation',
              f'Hi {data["user_name"]}, your booking at {data["time"]} {data["date"]} has been confirmed. '
              f'Thank you!',
              settings.EMAIL_HOST_USER,
              [data['user_email']])
    logger.info(f'Send email successfully...')
