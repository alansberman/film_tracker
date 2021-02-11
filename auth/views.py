import sys
from django.views.decorators.csrf import csrf_exempt
from films.models import Token
from django.shortcuts import render
import requests
import json
# Create your views here.
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# pylint:disable=relative-beyond-top-level
from datetime import datetime as dt
import datetime
from films.models import Token
sys.path.append('..')


@csrf_exempt
def obtain_token(request, *args, **kwargs):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    resp = obtain_jwt_token(request, *args, **kwargs)
    token = resp.data
    if token:
        user = authenticate(request, username=username, password=password)
        if user:
            user_object = User.objects.filter(username=username).first()
            # Check if the user already has a token
            # pylint:disable=no-member
            tkn = Token.objects.filter(
                user=user_object, valid=True)
            if tkn:
                return JsonResponse(data={'token': tkn['value']})
            expiration = timezone.now() + datetime.timedelta(hours=24)
            token_object = Token(user=user_object, value=token.get('token'), expiry=expiration,
                                 username=username, valid=True)
            token_object.save()
            return JsonResponse(data={
                'token': token,
            })
    return Response('Failed to generate token', status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def refresh_token(request, *args, **kwargs):
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization'].split(" ")[1]
        # pylint: disable=no-member
        token = Token.objects.filter(value=auth_token).first()
        if token:
            token.valid = False
            token.save()
            return Response('Token invalidated', status=200)
    return Response('Failed to invalidate token', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def logout(request):
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization'].split(" ")[1]
        # pylint: disable=no-member
        token = Token.objects.filter(value=auth_token).first()
        if token:
            token.valid = False
            token.save()
            return Response('Token invalidated', status=200)
    return Response('Failed to invalidate token', status=status.HTTP_400_BAD_REQUEST)
