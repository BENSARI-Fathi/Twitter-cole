from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import NotAuthenticated, IsOwnerOrReadOnly

from .serializers import (
    UserSerializer, MyTokenObtainPairSerializer,
    TweetSerializer, TweetLikeSerializer,
    FollowSerializer, TweetReplySerializer
)
from .models import (
    Tweet, TweetLike, Follow
)

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRegister(APIView):
    permission_classes = [NotAuthenticated]

    def post(self, request):
        data = request.data
        UserSerializer().validate_email(data['email'])
        if data['pw'] != data['confirmPw']:
            return Response(data={'detail': 'password must match !'}, status=HTTP_400_BAD_REQUEST)
        new_user = User(
            first_name=data['firstName'],
            last_name=data['lastName'],
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['pw'])
        new_user.save()
        refresh = RefreshToken.for_user(new_user)
        resp = UserSerializer(new_user, many=False, context={'request': request}).data
        resp['access'] = str(refresh.access_token)
        resp['refresh'] = str(refresh)
        return Response(resp)


class UploadUserAvatar(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, **kwargs):
        user = request.user
        user.avatar = request.FILES.get('image')
        user.save()
        refresh = RefreshToken.for_user(user)
        resp = UserSerializer(user, many=False, context={'request': request}).data
        resp['access'] = str(refresh.access_token)
        resp['refresh'] = str(refresh)
        return Response(resp)


class UploadUserBackIm(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, **kwargs):
        user = request.user
        user.backgroundIm = request.FILES.get('image')
        user.save()
        refresh = RefreshToken.for_user(user)
        resp = UserSerializer(user, many=False, context={'request': request}).data
        resp['access'] = str(refresh.access_token)
        resp['refresh'] = str(refresh)
        return Response(resp)


class UpdateUserApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, **kwargs):
        data = request.data
        user = request.user
        user.username = data['username']
        user.first_name = data['fullName'].split(' ')[0]
        user.last_name = data['fullName'].split(' ')[1]
        user.bio = data['bio']
        user.email = data['email']
        if data['pw'] != '':
            is_true = user.check_password(data['oldpw'])
            if is_true:
                if data['pw'] == data['confirmPw']:
                    user.set_password(data['pw'])
                return Response(data={'detail': 'Password didn\'t match !'}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'detail': 'Old Password is incorrect !'}, status=HTTP_400_BAD_REQUEST)
        user.save()
        refresh = RefreshToken.for_user(user)
        resp = UserSerializer(user, many=False, context={'request': request}).data
        resp['access'] = str(refresh.access_token)
        resp['refresh'] = str(refresh)
        return Response(resp)


class TweetListApiView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TweetSerializer
    queryset = Tweet.objects.filter(tweet_type='tweet')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TweetDetailsApiView(mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReplyTweetListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TweetReplySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        tweet = Tweet.objects.get(pk=pk)
        return Tweet.objects.get_reply(tweet)


class LikeTweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user
        pk = kwargs['pk']
        tweet = Tweet.objects.get(pk=pk)
        if tweet.tweetlike_set.filter(author=user).exists():
            return Response(data='You already liked this tweet', status=HTTP_400_BAD_REQUEST)
        tweet.num_likes += 1
        tweet.save()
        user.tweetlike.tweet.add(tweet)
        return Response('tweet liked !')


class DislikeTweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user
        pk = kwargs['pk']
        tweet = Tweet.objects.get(pk=pk)
        if not tweet.tweetlike_set.filter(author=user).exists():
            return Response(data='You can\'t perform this action', status=HTTP_400_BAD_REQUEST)
        tweet.num_likes -= 1
        tweet.save()
        user.tweetlike.tweet.remove(tweet)
        return Response('tweet disliked !')


class FollowRecommendationList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.non_following_user(user)


class UserTweetRetweet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        return user.tweet_set.select_related("parent")


class TweetLikeByUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        tweet_like = user.tweetlike
        resp = TweetLikeSerializer(tweet_like, many=False)
        return Response(resp.data)


class CreateTweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        image = request.FILES.get('image', None)
        new_tweet = Tweet.objects.create(
            author=user,
            content=data['content'],
            image=image,
        )
        resp = TweetSerializer(new_tweet, many=False, context={'request': request})
        return Response(resp.data)


class CommentTweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        data = request.data
        user = request.user
        pk = kwargs['pk']
        parent = Tweet.objects.get(pk=pk)
        image = request.FILES.get('image', None)
        new_comment = Tweet.objects.create(
            author=user,
            parent=parent,
            content=data['content'],
            image=image,
            tweet_type=data['tweet_type'],
        )
        parent.num_reply += 1
        parent.save()
        resp = TweetSerializer(new_comment, many=False, context={'request': request})
        return Response(resp.data)


class RTTweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user
        pk = kwargs['pk']
        parent = Tweet.objects.get(pk=pk)
        if Tweet.objects.has_already_retweet(parent, user):
            return Response(data={'detail': 'You already RT this tweet !'}, status=HTTP_400_BAD_REQUEST)
        Tweet.objects.create(
            author=user,
            parent=parent,
            tweet_type='rt',
        )
        parent.num_retweet += 1
        parent.save()
        return Response('successfully retweeted !')


class FollowUserApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user
        pk = kwargs['pk']
        user_to_follow = User.objects.get(pk=pk)
        if user.following.follow_user.filter(pk=pk).exists():
            return Response(data={'detail': 'You already follow this user'}, status=HTTP_400_BAD_REQUEST)
        user.following.follow_user.add(user_to_follow)
        user_to_follow.followerNum += 1
        user.followingNum += 1
        user.save()
        user_to_follow.save()
        return Response('successfully Done !')


class UnfollowUserApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user
        pk = kwargs['pk']
        user_to_follow = User.objects.get(pk=pk)
        if not user.following.follow_user.filter(pk=pk).exists():
            return Response(data={'detail': 'You can\'t perform this action'}, status=HTTP_400_BAD_REQUEST)
        user.following.follow_user.remove(user_to_follow)
        user_to_follow.followerNum -= 1
        user.followingNum -= 1
        user.save()
        user_to_follow.save()
        return Response('successfully Done !')


class UserFollowingList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        return Follow.objects.following(user)


class UserFollowersList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        return user.followers.all()

# add follow user option
