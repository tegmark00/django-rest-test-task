from django.urls import path
from .views import PostAPIView, PostLikeAPIView, LikeAnalyticsAPIView

urlpatterns = [
    path('post/', PostAPIView.as_view(), name='api-post'),
    path('post/like/<int:post_id>/', PostLikeAPIView.as_view(), name='api-post-like'),
    path('analytics/', LikeAnalyticsAPIView.as_view(), name='api-post-like'),
]
