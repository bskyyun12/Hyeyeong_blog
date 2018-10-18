from django.conf import settings
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from multiselectfield import MultiSelectField

EMOTICONS = (
    ('happy', 'Happy'),
    ('sleepy', 'Sleepy'),
    ('sick', 'Sick'),
    ('angry', 'Angry'),
    ('bored', 'Bored'),
    ('laugh', 'Laugh'),
    ('love', 'Love'),
    ('pout', 'Pout'),
    ('sad', 'Sad'),
)

# Create your models here.
class Calendar(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    emoticon = MultiSelectField(choices=EMOTICONS, max_choices=3)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

# Calendar comment
class Comment(models.Model):
    post = models.ForeignKey('album.Calendar', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # author = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} - {self.comment}'

# Calendar images
class Image(models.Model):
    post = models.ForeignKey('album.Calendar', related_name='images', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='calendar_image/%Y/%m')
    thumbnail = ImageSpecField(
		source = 'image',
		processors = [ResizeToFill(700, 700)], # 처리할 작업 목룍
		format = 'JPEG',					# 최종 저장 포맷
		options = {'quality': 60})  		# 저장 옵션
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='image_likes')

    def __str__(self):
        return f'{self.post.title}\'s image'

    def total_likes(self):
        return self.likes.count()


# Calendar comment
class ImageComment(models.Model):
    image = models.ForeignKey('album.Image', related_name='image_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # author = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='image_replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image} - {self.comment}'

class Friend(models.Model):
    # related_name의 default는 related_name='friend_set'이므로 중복되지 않도록  이름을 지어준것
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.CASCADE)

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

class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    post = models.ForeignKey('album.Calendar', related_name='post_notification', blank=True, null=True, on_delete=models.CASCADE)
    post_comment =  models.ForeignKey('album.Comment', related_name='post_comments_notification', blank=True, null=True, on_delete=models.CASCADE)
    image = models.ForeignKey('album.Image', related_name='image_notification', blank=True, null=True, on_delete=models.CASCADE)
    image_comment = models.ForeignKey('album.ImageComment', related_name='image_comments_notification', blank=True, null=True, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} --> {self.receiver}'
