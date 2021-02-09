from django.urls import path
from .views import CreateUserAPIView, AuthenticateUserAPIView, MyActivityAPIView

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='user-create'),
    path('auth/', AuthenticateUserAPIView.as_view(), name='user-auth'),
    path('activity/', MyActivityAPIView.as_view(), name='my-activity')
]
