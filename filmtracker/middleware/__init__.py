from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
from films.models import Token
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# pylint:disable=relative-beyond-top-level
from django.contrib.auth import authenticate, login

from datetime import datetime as dt
import datetime
import sys
sys.path.append('..')


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)

        return response

    def process_request(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization'].split(" ")[1]
            # pylint: disable=no-member
            token = Token.objects.filter(value=auth_token).first()
            if token:
                is_valid = timezone.now() < token.expiry
                if not is_valid:
                    token.valid = False
                    token.save(update_fields=['valid'])
                user = User.objects.filter(id=token.user.id).first()
                if is_valid and user:
                    login(request, user)
                    request.user = user

        return self.get_response(request)
