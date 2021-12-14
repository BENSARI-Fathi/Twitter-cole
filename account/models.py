from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def upload_avatar_image(instance, filename):
    return f"avatar/{instance}/{filename}"


def upload_background_image(instance, filename):
    return f"background/{instance}/{filename}"


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True, null=True, default='')
    followerNum = models.IntegerField(blank=True, null=True, default=0)
    followingNum = models.IntegerField(blank=True, null=True, default=0)
    isVerified = models.BooleanField(default=False, blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_avatar_image, default='avatar.png', blank=True)
    backgroundIm = models.ImageField(upload_to=upload_background_image, default='placeholder.png', blank=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# superuser: fethibensari@gmail.com ; pw: twitterclone