from django.urls import path
from .views import (
    MovieStreamView,
    EpisodeStreamView,
    MovieSubtitlesView,
    EpisodeSubtitlesView,
)

urlpatterns = [
    path('movies/<int:movie_id>/stream/', MovieStreamView.as_view(), name='movie-stream'),
    path('episodes/<int:episode_id>/stream/', EpisodeStreamView.as_view(), name='episode-stream'),
    path('movies/<int:movie_id>/subtitles/', MovieSubtitlesView.as_view(), name='movie-subtitles'),
    path('episodes/<int:episode_id>/subtitles/', EpisodeSubtitlesView.as_view(), name='episode-subtitles'),
]
