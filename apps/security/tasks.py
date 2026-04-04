from celery import shared_task
from infrastructure.email.email_service import send_email
import logging

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def send_email_task(self, to_email, subject, message):
    try:
        logger.info(f"Sending email to {to_email}")

        send_email(
            to_email=to_email,
            subject=subject,
            message=message
        )

        logger.info(f"Email sent to {to_email}")

    except Exception as exc:
        logger.warning(f"Retry {self.request.retries + 1}")

        raise self.retry(exc=exc)