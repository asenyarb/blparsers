from django.db import models
from django.contrib.auth.models import AbstractUser

from djchoices import DjangoChoices, ChoiceItem


class User(AbstractUser):
    pass


class Publication(models.Model):
    class Status(DjangoChoices):
        Draft = ChoiceItem('draft')
        Published = ChoiceItem('published')
        Unpublished = ChoiceItem('unpublished')

    external_id = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    text_hash = models.CharField(max_length=33)
    link = models.CharField(max_length=256)
    created_date = models.DateTimeField(blank=True)
    telegram_message_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.Draft
    )


class PublicationPhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="phones")
