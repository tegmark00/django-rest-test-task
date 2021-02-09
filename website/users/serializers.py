from django.contrib.auth.signals import user_logged_in
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_jwt.utils import jwt_payload_handler

from .models import User
from .constants import AUTH_FAILED, EMAIL_EXISTS


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        try:
            User.objects.get(email=value.lower())
        except ObjectDoesNotExist:
            return value.lower()
        raise ValidationError(EMAIL_EXISTS)


class AuthenticateJWTUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=40)
    password = serializers.CharField(max_length=128)

    def save(self, **kwargs):
        pass

    def login(self) -> str:
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            return self.create_token(user)
        except ObjectDoesNotExist:
            raise ValidationError(AUTH_FAILED)

    @staticmethod
    def create_token(user: User):
        assert isinstance(user, User)
        payload = jwt_payload_handler(user)
        return {
            'name': f"{user.first_name} {user.last_name}",
            'token': jwt.encode(payload, settings.SECRET_KEY),
        }