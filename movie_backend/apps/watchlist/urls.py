from django.urls import path
from .views import (
    WatchlistView,
    WatchlistDetailView,
    FavoritesView,
    FavoriteDetailView,
)

urlpatterns = [
    path('watchlist/', WatchlistView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchlistDetailView.as_view(), name='watchlist-delete'),
    path('favorites/', FavoritesView.as_view(), name='favorites-list-create'),
    path('favorites/<int:pk>/', FavoriteDetailView.as_view(), name='favorites-delete'),
]
