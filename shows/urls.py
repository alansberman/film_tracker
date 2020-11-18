from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/view', views.get_show, name='view'),
    path('popular', views.popular, name='popular'),
    path('<int:show_id>/add', views.add_show, name='add'),
    path('<int:id>/season/<int:season_number>',
         views.get_season, name='season'),
    path('<int:id>/season/<int:season_number>/episode/<int:episode_number>',
         views.get_episode, name='episode'),
    path('search', views.search, name='search'),
    path('<int:show_id>/wishlist',
         views.wishlist_show, name='wishlist-show'),
    path('wishlist', views.wishlist, name='wishlist-index'),
]
