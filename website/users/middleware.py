from django.http.request import HttpRequest
from django.shortcuts import reverse
from .models import User


class LastServiceAccess:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        path = request.path
        cond = hasattr(request, 'user')
        cond = cond and isinstance(request.user, User)
        cond = cond and path != reverse('my-activity')
        if cond:
            user: User = request.user
            user.update_last_access(path)
        return response
