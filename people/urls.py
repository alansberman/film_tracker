from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/view', views.get_person, name='view-person'),


]
