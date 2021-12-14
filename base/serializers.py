from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import (TweetLike, Tweet, Follow)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'avatar',
            'backgroundIm',
            'bio',
            'username',
            'isVerified',
            'full_name',
            'followerNum',
            'followingNum',
            'date_joined',
        ]

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError({'detail': 'User with this email already exist !'})
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user, context=self.context).data
        for k, v in serializer.items():
            data[k] = v
        return data


class NestedTweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    parent = NestedTweetSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'


class TweetReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'

    def create(self, validated_data):
        tweet = Tweet.objects.create(
            author=self.context['request'].user,
            parent=validated_data['parent'],
            content=validated_data['content'],
            image=validated_data['image'],
            tweet_type=validated_data['tweet_type'],
        )
        return tweet


class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'user')
