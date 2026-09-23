from django.urls import path
from .views import (
    MovieReviewsView,
    SeriesReviewsView,
    ReviewDetailView,
)

urlpatterns = [
    path('movies/<int:movie_id>/reviews/', MovieReviewsView.as_view(), name='movie-reviews'),
    path('series/<int:series_id>/reviews/', SeriesReviewsView.as_view(), name='series-reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
