from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from .static import MAX_DELIVERY_RETRIES


@shared_task(bind=True, max_retries=MAX_DELIVERY_RETRIES)
def deliver_message(self, message):
    success = message.deliver()
    if not success:
        try:
            self.retry(countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            message.mark_as_failed()