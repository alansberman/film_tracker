from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('<int:movie_id>/add', views.add_movie, name='add'),
    path('<int:id>/view', views.get_film, name='view'),
    path('people/<int:id>/view', views.get_person, name='view-person'),


]
