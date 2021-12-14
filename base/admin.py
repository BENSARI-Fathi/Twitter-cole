from django.contrib import admin
from .models import (Tweet, TweetLike, Follow)
# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweetLike)
admin.site.register(Follow)