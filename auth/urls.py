from django.urls import path

from . import views


urlpatterns = [
    path('obtain_token', views.obtain_token, name='obtain-token'),
    path('refresh_token', views.refresh_token, name='refresh-token'),
    path('logout', views.logout, name='logout'),

]
