from django.db import models


# Create your models here.
class Post(models.Model):
    external_id = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    text_hash = models.CharField(max_length=33)
    link = models.CharField(max_length=256)
    created_date = models.DateTimeField(blank=True)


class PhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="phones")
