from django.db import models
from django.utils import timezone


class Image(models.Model):
    image =models.ImageField(upload_to='img')
    create_date = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return self.image