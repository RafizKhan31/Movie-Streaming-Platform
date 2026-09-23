from django.db import models
from django.conf import settings
from apps.movies.models import Movie
from apps.tv.models import Episode


class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='history_records')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True, related_name='history_records')
    current_position = models.FloatField('Current Position (seconds)', default=0.0)
    duration = models.FloatField('Total Duration (seconds)', default=1.0)
    completed = models.BooleanField('Watched to End', default=False)
    last_watched = models.DateTimeField('Last Watched', auto_now=True)

    class Meta:
        verbose_name = 'Watch History'
        verbose_name_plural = 'Watch History'
        ordering = ['-last_watched']
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], condition=models.Q(movie__isnull=False), name='unique_user_movie_history'),
            models.UniqueConstraint(fields=['user', 'episode'], condition=models.Q(episode__isnull=False), name='unique_user_episode_history'),
        ]

    def __str__(self):
        item = self.movie.title if self.movie else str(self.episode)
        return f"{self.user.username} watched {item} ({self.progress_percentage}%)"

    @property
    def progress_percentage(self):
        if self.duration > 0:
            pct = round((self.current_position / self.duration) * 100, 1)
            return min(100.0, max(0.0, pct))
        return 0.0

    @property
    def progress_display(self):
        watched_mins = int(self.current_position // 60)
        total_mins = int(self.duration // 60)
        return f"Watched: {watched_mins} minutes of {total_mins} minutes (Progress: {self.progress_percentage}%)"

    def save(self, *args, **kwargs):
        # Automatically mark as completed if reached > 90%
        if self.progress_percentage >= 90.0:
            self.completed = True
        super().save(*args, **kwargs)
