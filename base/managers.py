from django.db import models
from django.db.models import Count
from django.db.models import Q


class FollowManager(models.Manager):
    def following(self, user):
        follow_obj = self.get_queryset().get(user=user)
        return follow_obj.follow_user.all()

    def following_number(self, user):
        return self.following(user).count()

    def non_following_user(self, user):
        following_list = self.following(user)
        UserClass = user.__class__
        return UserClass.objects.exclude(pk=user.id).difference(following_list)[:5]


class TweetManager(models.Manager):
    def has_already_retweet(self, tweet, user):
        return self.get_queryset().filter(Q(tweet_type='rt') &
                                          Q(parent=tweet) &
                                          Q(author=user)).exists()

    def get_reply(self, tweet):
        return self.get_queryset().filter(Q(tweet_type='reply') &
                                          Q(parent=tweet))
