from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('popular', views.popular, name='popular'),
    path('upcoming', views.upcoming, name='upcoming'),
    path('festivals', views.festivals, name='festivals'),
    path('statistics', views.statistics, name='statistics'),
    path('top', views.top, name='top'),
    path('<int:movie_id>/add', views.add_movie, name='add'),
    path('<int:movie_id>/wishlist',
         views.wishlist_movie, name='wishlist-film'),
    path('wishlist', views.wishlist, name='wishlist-index'),
    path('<int:id>/like', views.like, name='like'),
    path('<int:id>/dislike', views.dislike, name='dislike'),
    path('<int:id>/view', views.get_film, name='view'),
    path('chart', views.years_chart, name='years-chart'),
    path('runtime-chart', views.runtime_chart, name='runtime-chart'),
    path('decades-chart', views.decades_chart, name='decades-chart'),
    path('ratings-chart', views.ratings_chart, name='ratings-chart'),
    path('genres', views.genres, name='genres'),
    path('discover', views.discover, name='discover'),


]
