from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.movies.models import Movie
from apps.tv.models import TVSeries


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        'Rating (1-10)',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating on a scale of 1 to 10",
    )
    title = models.CharField('Review Headline', max_length=255, blank=True)
    content = models.TextField('Review Content', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rating & Review'
        verbose_name_plural = 'Ratings & Reviews'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], condition=models.Q(movie__isnull=False), name='unique_user_movie_review'),
            models.UniqueConstraint(fields=['user', 'series'], condition=models.Q(series__isnull=False), name='unique_user_series_review'),
        ]

    def __str__(self):
        target = self.movie.title if self.movie else self.series.title
        return f"{self.user.username} - {target}: {self.rating}/10"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_average_rating()

    def delete(self, *args, **kwargs):
        movie = self.movie
        series = self.series
        super().delete(*args, **kwargs)
        if movie:
            avg = movie.reviews.aggregate(models.Avg('rating'))['rating__avg']
            if avg:
                movie.imdb_rating = round(avg, 1)
                movie.save(update_fields=['imdb_rating'])
        elif series:
            avg = series.reviews.aggregate(models.Avg('rating'))['rating__avg']
            if avg:
                series.imdb_rating = round(avg, 1)
                series.save(update_fields=['imdb_rating'])

    def update_average_rating(self):
        if self.movie:
            avg = self.movie.reviews.aggregate(models.Avg('rating'))['rating__avg']
            if avg:
                self.movie.imdb_rating = round(avg, 1)
                self.movie.save(update_fields=['imdb_rating'])
        elif self.series:
            avg = self.series.reviews.aggregate(models.Avg('rating'))['rating__avg']
            if avg:
                self.series.imdb_rating = round(avg, 1)
                self.series.save(update_fields=['imdb_rating'])
