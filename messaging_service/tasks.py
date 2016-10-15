from celery import shared_task


@shared_task(bind=True, max_retries=10)
def deliver_message(self, message):
    try:
        return message.message
    except ValueError as exc:
        self.retry(exc=exc, countdown=2 ** self.request.retries)
    return True
