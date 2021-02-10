from dateparser import parse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from django.utils.timezone import make_aware
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Post, PostLike
from .serializers import PostSerializer, PostLikeSerializer, PostLikeAnalyticsSerializer


class PostAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeAPIView(generics.GenericAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        like, created = PostLike.objects.get_or_create(user=request.user, post=get_object_or_404(Post, id=post_id))
        if created:
            return Response(data={'status': 'You liked this post'}, status=status.HTTP_201_CREATED)
        like.delete()
        return Response(data={'status': 'You unliked this post'}, status=status.HTTP_201_CREATED)


class LikeAnalyticsAPIView(generics.GenericAPIView):
    serializer_class = PostLikeAnalyticsSerializer

    def get_rows(self, params):
        date_from = params.get('date_from')
        date_to = params.get('date_to')
        if isinstance(date_from, date) and isinstance(date_to, date):
            qs = PostLike.objects.values('created_at__date').\
                filter(created_at__range=[date_from, date_to])
        elif isinstance(date_from, date):
            qs = PostLike.objects.values('created_at__date').\
               filter(created_at__gte=date_from)
        elif isinstance(date_to, date):
            qs = PostLike.objects.values('created_at__date').\
               filter(created_at__lte=date_to)
        else:
            qs = PostLike.objects.values('created_at__date')

        return qs.values('created_at__date').\
            annotate(total_likes=Count('id')). \
            values('created_at__date', 'total_likes'). \
            order_by('created_at__date')

    def get(self, request, *args, **kwargs):
        serializer = PostLikeAnalyticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(self.get_rows(serializer.validated_data))
