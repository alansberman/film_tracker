from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/view', views.get_person, name='view'),
    path('<int:id>/like', views.like_person, name='like'),
    path('liked', views.liked_people, name='liked'),
    path('search', views.search, name='search'),

]
