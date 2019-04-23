from django.db import models
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField(upload_to='img', blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    img_hash = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['id']
