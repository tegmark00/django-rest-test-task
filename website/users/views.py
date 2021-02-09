from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, AuthenticateJWTUserSerializer
from .models import User


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthenticateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest):
        fields = request.data
        serializer = AuthenticateJWTUserSerializer(data=fields)
        serializer.is_valid(raise_exception=True)
        auth_token = serializer.login()
        return Response(auth_token, status=status.HTTP_200_OK)


class MyActivityAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest):
        user: User = request.user
        return Response({
            'last_login': user.last_login,
            'last_api_access_path': user.last_api_access_path,
            'last_api_access_date': user.last_api_access_date
        })
