from django.db import models

from website.users.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    text = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ["-created_at"]


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name='likes')
    post = models.ForeignKey(Post, related_name='likes')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'post like'
        verbose_name_plural = 'post likes'
        ordering = ["-created_at"]
