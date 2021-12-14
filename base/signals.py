from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TweetLike, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_relationship_instance(sender, instance, created, **kwargs):
    if created:
        print('am called !')
        TweetLike.objects.create(author=instance)
        Follow.objects.create(user=instance)