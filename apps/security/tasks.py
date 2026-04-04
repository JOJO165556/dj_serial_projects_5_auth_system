from celery import shared_task
from infrastructure.email.email_service import send_email

@shared_task
def send_email_task(to_email, subject, message):
    send_email(
        to_email=to_email,
        subject=subject,
        message=message
    )