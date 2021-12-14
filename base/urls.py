from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserListApiView, TweetListApiView,
    LikeTweetApiView, DislikeTweetApiView,
    MyTokenObtainPairView, UploadUserAvatar,
    UploadUserBackIm, UpdateUserApi,
    FollowRecommendationList, UserTweetRetweet,
    TweetLikeByUser, CreateTweetApiView,
    CommentTweetApiView, RTTweetApiView,
    FollowUserApiView, UnfollowUserApiView,
    UserDetailApiView, UserFollowingList,
    UserFollowersList, UserRegister,
    TweetDetailsApiView, ReplyTweetListApiView,
)

urlpatterns = [
    path('users/', UserListApiView.as_view()),
    path('users/recommendation/', FollowRecommendationList.as_view()),
    path('user/update/', UpdateUserApi.as_view()),
    path('user/update/avatar/', UploadUserAvatar.as_view()),
    path('user/update/backimage/', UploadUserBackIm.as_view()),
    path('user/tweets/like/', TweetLikeByUser.as_view()),
    path('user/register/', UserRegister.as_view()),
    path('user/<int:pk>/tweets/', UserTweetRetweet.as_view()),
    path('user/<int:pk>/', UserDetailApiView.as_view()),

    path('tweets/', TweetListApiView.as_view()),
    path('tweet/add/', CreateTweetApiView.as_view()),
    path('tweet/<int:pk>/', TweetDetailsApiView.as_view()),
    path('tweet/<int:pk>/like', LikeTweetApiView.as_view()),
    path('tweet/<int:pk>/dislike', DislikeTweetApiView.as_view()),
    path('tweet/<int:pk>/comment', CommentTweetApiView.as_view()),
    path('tweet/<int:pk>/retweet', RTTweetApiView.as_view()),
    path('tweet/<int:pk>/reply', ReplyTweetListApiView.as_view()),

    path('follow/user/<int:pk>/', FollowUserApiView.as_view()),
    path('unfollow/user/<int:pk>/', UnfollowUserApiView.as_view()),
    path('following/user/<int:pk>/', UserFollowingList.as_view(), name='list_following_user'),
    path('followers/user/<int:pk>/', UserFollowersList.as_view(), name='list_followers_user'),

    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
