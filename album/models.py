from django.conf import settings
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Calendar(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='calendar_image/%Y/%m')
    emoticon = models.CharField(max_length=100)
    image_thumbnail = ImageSpecField(
		source = 'image',
		processors = [ResizeToFill(700, 700)], # 처리할 작업 목룍
		format = 'JPEG',					# 최종 저장 포맷
		options = {'quality': 60})  		# 저장 옵션


    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('album.Calendar', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.post} - {self.comment}'

class Friend(models.Model):
    # related_name의 default는 related_name='friend_set'이므로 중복되지 않도록  이름을 지어준것
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.DO_NOTHING)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)
