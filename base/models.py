from django.db import models
from django.contrib.auth import get_user_model
from .managers import FollowManager, TweetManager

# Create your models here.
User = get_user_model()


def upload_tweet_image(instance, filename):
    return f"tweet/{instance.author}/{filename}"


class Tweet(models.Model):
    TWEET = 'tweet'
    REPLY = 'reply'
    RETWEET = 'rt'

    TWEET_TYPE = [
        (TWEET, 'tweet'),
        (REPLY, 'reply'),
        (RETWEET, 'rt'),
    ]

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='reply')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_tweet_image)
    tweet_type = models.CharField(max_length=5, choices=TWEET_TYPE, default=TWEET)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_likes = models.IntegerField(blank=True, default=0)
    num_reply = models.IntegerField(blank=True, default=0)
    num_retweet = models.IntegerField(blank=True, default=0)

    objects = TweetManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} {self.tweet_type} {self.created_at.strftime("Created on %d, %b %Y")}'


class TweetLike(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    tweet = models.ManyToManyField(Tweet, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} like lists"


class Follow(models.Model):
    user = models.OneToOneField(User, related_name='following', on_delete=models.CASCADE)
    follow_user = models.ManyToManyField(User, related_name='followers', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = FollowManager()

    def __str__(self):
        return f'{self.user} following lists'


"""
    faiza@mail.com ; pw: bensari1996
    mahmoud@yahoo.dz ; pw: bensari1996
    redouane@mail.com ; pw: bensari1996
    farida@mail.com ; bensari1996
"""
