from dateparser import parse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
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
        try:
            like, created = PostLike.objects.get_or_create(user=request.user, post=Post.objects.get(id=post_id))
            if created:
                return Response(data={'status': 'You liked this post'}, status=status.HTTP_201_CREATED)
            like.delete()
            return Response(data={'status': 'You unliked this post'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(data={'status': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class LikeAnalyticsAPIView(generics.GenericAPIView):

    queryset = None
    serializer_class = None

    def get_queryset(self):
        date_from = parse(self.request.GET.get('date_from')).replace(tzinfo=timezone.utc)
        date_to = parse(self.request.GET.get('date_to')).replace(tzinfo=timezone.utc)
        if date_from and date_to:
            return PostLike.objects.values('created_at__date').\
                annotate(total_likes=Count('id')).\
                values('created_at__date', 'total_likes').\
                order_by('created_at__date')
        return PostLike.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            return Response(self.get_queryset())
        except:
            return Response({'error': 'Invalid parameters for date'}, status.HTTP_400_BAD_REQUEST)
