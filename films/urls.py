from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('popular', views.popular, name='popular'),
    path('upcoming', views.upcoming, name='upcoming'),
    path('top', views.top, name='top'),
    path('<int:movie_id>/add', views.add_movie, name='add'),
    path('<int:movie_id>/wishlist',
         views.wishlist_movie, name='wishlist-film'),
    path('wishlist', views.wishlist, name='wishlist-index'),
    path('<int:id>/view', views.get_film, name='view'),
]
