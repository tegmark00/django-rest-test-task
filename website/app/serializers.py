from collections import OrderedDict
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware

from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'user']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post']


class PostLikeAnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateField(format='%Y-%m-%d', required=False)
    date_to = serializers.DateField(format='%Y-%m-%d', required=False)
