from django.urls import path
from .views import (
    TVSeriesListView,
    TVSeriesDetailView,
    TVSeriesSeasonsView,
    TVSeriesEpisodesView,
    EpisodeDetailView,
)

urlpatterns = [
    path('series/', TVSeriesListView.as_view(), name='series-list'),
    path('series/<str:identifier>/', TVSeriesDetailView.as_view(), name='series-detail'),
    path('series/<str:identifier>/seasons/', TVSeriesSeasonsView.as_view(), name='series-seasons'),
    path('series/<str:identifier>/episodes/', TVSeriesEpisodesView.as_view(), name='series-episodes'),
    path('tv/', TVSeriesListView.as_view(), name='tv-list'),
    path('tv/<str:identifier>/', TVSeriesDetailView.as_view(), name='tv-detail'),
    path('tv/<str:identifier>/seasons/', TVSeriesSeasonsView.as_view(), name='tv-seasons'),
    path('tv/<str:identifier>/episodes/', TVSeriesEpisodesView.as_view(), name='tv-episodes'),
    path('episodes/<int:pk>/', EpisodeDetailView.as_view(), name='episode-detail'),
]
