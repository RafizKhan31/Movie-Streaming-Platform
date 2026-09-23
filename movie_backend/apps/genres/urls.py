from django.urls import path
from .views import GenreListView, GenreDetailView, GenreMoviesView

urlpatterns = [
    path('', GenreListView.as_view(), name='genre-list'),
    path('<slug:slug>/', GenreDetailView.as_view(), name='genre-detail'),
    path('<slug:slug>/movies/', GenreMoviesView.as_view(), name='genre-movies'),
]
