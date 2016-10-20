from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .static import MESSAGE_STATUS, MESSAGE_STATUS_DICT
from .tasks import deliver_message
from requests.exceptions import RequestException
import requests


# Create your models here.


class Message(models.Model):
    message = models.TextField()
    url = models.URLField(max_length=1000)
    status = models.PositiveSmallIntegerField(choices=MESSAGE_STATUS, default=MESSAGE_STATUS_DICT['queued'], editable=False)

    def __str__(self):
        return str(self.id) + "|" + self.message + "|" + self.humanized_status()

    def deliver(self):
        if self.already_processed():
            return True
        try:
            requests.post(self.url, data=self.message)
        except RequestException as e:
            return False
        else:
            self.mark_as_sent()
            return True

    def already_processed(self):
        if self.status != MESSAGE_STATUS_DICT['queued']:
            return True
        else:
            return False

    def mark_as_sent(self):
        self.status = MESSAGE_STATUS_DICT['sent']
        self.save()

    def mark_as_delivered(self):
        self.status = MESSAGE_STATUS_DICT['delivered']
        self.save()

    def mark_as_failed(self):
        self.status = MESSAGE_STATUS_DICT['failed']
        self.save()

    def humanized_status(self):
        return MESSAGE_STATUS[self.status][1]

@receiver(post_save, sender=Message, dispatch_uid="enqueue_for_delivery")
def enqueue_for_delivery(sender, instance, created, **kwargs):
    if instance.status == MESSAGE_STATUS_DICT['queued'] and created:
        deliver_message.delay(instance)
