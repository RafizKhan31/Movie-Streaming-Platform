from django.db import models
from django.conf import settings
from apps.movies.models import Movie
from apps.tv.models import TVSeries


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='watchlist_items')
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, null=True, blank=True, related_name='watchlist_items')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Watchlist Item'
        verbose_name_plural = 'Watchlist Items'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], condition=models.Q(movie__isnull=False), name='unique_user_movie_watchlist'),
            models.UniqueConstraint(fields=['user', 'series'], condition=models.Q(series__isnull=False), name='unique_user_series_watchlist'),
        ]

    def __str__(self):
        item = self.movie.title if self.movie else self.series.title
        return f"{self.user.username} Watchlist: {item}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='favorite_items')
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, null=True, blank=True, related_name='favorite_items')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favorite Item'
        verbose_name_plural = 'Favorites'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], condition=models.Q(movie__isnull=False), name='unique_user_movie_favorite'),
            models.UniqueConstraint(fields=['user', 'series'], condition=models.Q(series__isnull=False), name='unique_user_series_favorite'),
        ]

    def __str__(self):
        item = self.movie.title if self.movie else self.series.title
        return f"{self.user.username} Favorite: {item}"
