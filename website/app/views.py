from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Post, PostLike
from .serializers import PostSerializer, PostLikeSerializer


class PostAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
        except ObjectDoesNotExist as e:
            return Response(data={'status': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)
