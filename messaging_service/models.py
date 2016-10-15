from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .static import MESSAGE_STATUS
from .tasks import deliver_message

# Create your models here.


class Message(models.Model):
    message = models.TextField()
    url = models.URLField(max_length=1000)
    status = models.PositiveSmallIntegerField(choices=MESSAGE_STATUS)


@receiver(post_save, sender=Message, dispatch_uid="enqueue_for_delivery")
def enqueue_for_delivery(sender, instance, created, **kwargs):
    if created:
        deliver_message.delay(instance)


