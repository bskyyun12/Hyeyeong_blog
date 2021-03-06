from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import Resize

# Extending the base User manager that Django uses for its original UserManager.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    # Defining the same 3 methods that the original Django UserManager has.
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    # make first_name as case insenditive
    def filter(self, **kwargs):
        if 'first_name' in kwargs:
            kwargs['first_name__iexact'] = kwargs['first_name']
            del kwargs['first_name']
        return super(UserManager, self).filter(**kwargs)

    def get(self, **kwargs):
        if 'first_name' in kwargs:
            kwargs['first_name__iexact'] = kwargs['first_name']
            del kwargs['first_name']
        return super(UserManager, self).get(**kwargs)


# Extending the base class that Django has for User models.
class User(AbstractUser):
    """User model."""

    # Removing the username field.
    username = None
    # Making the email, first_name field required and unique.
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), unique=True, max_length=20)

    # Telling Django that you are going to use the email field as the USERNAME_FIELD.
    USERNAME_FIELD = 'email'
    # Removing the email field from the REQUIRED_FIELDS settings (it is automatically included as USERNAME_FIELD).
    REQUIRED_FIELDS = []
    # Assigning the new Manager to the User model.
    objects = UserManager()


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='Sodra Sandby')


class UserProfile(models.Model):
    # From Django 2.0 on_delete is required
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(blank=True, max_length=100, default='')
    city = models.CharField(blank=True, max_length=100, default='')
    website = models.URLField(blank=True, default='')
    phone = models.CharField(blank=True, max_length=20, default='')
    image = models.ImageField(upload_to='profile_image', blank=True, default='profile_image/flower.png')
    image_thumbnail = ImageSpecField(
		source = 'image',
		processors = [Resize(700, 700)], # 처리할 작업 목룍
		format = 'JPEG',					# 최종 저장 포맷
		options = {'quality': 60})  		# 저장 옵션

    # Sodra_Sandby가 도시인 유저만 보이게 하고싶을때
    # Sodra_Sandby = UserProfileManager()
    objects = models.Manager()

    # user.userprofile 리턴값을 이름으로
    def __str__(self):
        return self.user.email

# User가 생성되면 UserProfile을 생성
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)

class BabyProfile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    born_weight = models.IntegerField(default=0)
    born_height = models.IntegerField(default=0)
    born_location = models.CharField(max_length=20, blank=True)
    birthday = models.DateTimeField()
    image = models.ImageField(upload_to='baby_profile_image', blank=True, default='profile_image/flower.png')
    image_thumbnail = ImageSpecField(
		source = 'image',
		processors = [Resize(700, 700)], # 처리할 작업 목룍
		format = 'JPEG',					# 최종 저장 포맷
		options = {'quality': 60})  		# 저장 옵션

    def __str__(self):
        return str(self.first_name)+str(self.last_name)

class Milestone(models.Model):
    milestone = models.CharField(max_length=30)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=50)
