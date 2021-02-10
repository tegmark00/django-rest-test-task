import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_jwt.utils import jwt_payload_handler
from django.contrib.auth.hashers import check_password

from .models import User
from .constants import AUTH_FAILED, EMAIL_EXISTS, PASSWORD_INCORRECT


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        try:
            User.objects.get(email=value.lower())
        except ObjectDoesNotExist:
            return value.lower()
        raise ValidationError(EMAIL_EXISTS)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthenticateJWTUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=40)
    password = serializers.CharField(max_length=128)

    def validate_email(self, email):
        return email.lower()

    def login(self) -> str:
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            return self.create_token(user)
        raise ValidationError(AUTH_FAILED)

    @staticmethod
    def create_token(user: User):
        assert isinstance(user, User)
        payload = jwt_payload_handler(user)
        return {
            'name': f"{user.first_name} {user.last_name}",
            'token': jwt.encode(payload, settings.SECRET_KEY),
        }