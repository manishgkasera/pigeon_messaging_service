from celery import Celery

app = Celery('tasks', broker='redis://localhost', backend='redis://localhost')


@app.task(bind=True, max_retries=10)
def add(self, x, y):
    try:
        raise ValueError('A very specific bad thing happened')
    except ValueError as exc:
        self.retry(exc=exc, countdown=2 ** self.request.retries)
    return x + y
