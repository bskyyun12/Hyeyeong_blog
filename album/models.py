from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Calendar(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='calendar_image/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.title} - {self.date}'

class Comment(models.Model):
    post = models.ForeignKey('album.Calendar', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
