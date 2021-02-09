from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

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


class PostLikeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'