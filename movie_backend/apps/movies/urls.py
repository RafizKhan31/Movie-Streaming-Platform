from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    MovieTrendingView,
    MoviePopularView,
    MovieLatestView,
    MovieFeaturedView,
    MovieTopRatedView,
    MovieSubmitView,
)

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('trending/', MovieTrendingView.as_view(), name='movie-trending'),
    path('popular/', MoviePopularView.as_view(), name='movie-popular'),
    path('latest/', MovieLatestView.as_view(), name='movie-latest'),
    path('featured/', MovieFeaturedView.as_view(), name='movie-featured'),
    path('top-rated/', MovieTopRatedView.as_view(), name='movie-top-rated'),
    path('submit/', MovieSubmitView.as_view(), name='movie-submit'),
    path('<str:identifier>/', MovieDetailView.as_view(), name='movie-detail'),
]
