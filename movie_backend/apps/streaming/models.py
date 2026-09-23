from django.db import models
from apps.movies.models import Movie
from apps.tv.models import Episode


class VideoSource(models.Model):
    QUALITY_CHOICES = (
        ('360p', '360p (SD)'),
        ('480p', '480p (SD)'),
        ('720p', '720p (HD)'),
        ('1080p', '1080p (Full HD)'),
        ('4k', '4K (Ultra HD)'),
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='video_sources')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True, related_name='episode_video_sources')
    quality = models.CharField('Video Quality', max_length=20, choices=QUALITY_CHOICES, default='720p')
    file = models.FileField('Video File', upload_to='streaming/videos/', null=True, blank=True)
    source_url = models.URLField('External Video Stream URL / CDN', blank=True, max_length=1000)
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Video Source'
        verbose_name_plural = 'Video Sources'
        ordering = ['quality']

    def __str__(self):
        target = self.movie.title if self.movie else str(self.episode)
        return f"{target} [{self.quality}]"

    @property
    def stream_url(self):
        if self.file:
            return self.file.url
        return self.source_url


class Subtitle(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='subtitles')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True, related_name='episode_subtitles')
    language = models.CharField('Language Code', max_length=10, default='en', help_text="e.g. en, bn, hi, es")
    label = models.CharField('Language Label', max_length=50, default='English', help_text="e.g. English, Bengali, Hindi")
    subtitle_file = models.FileField('Subtitle File (.vtt or .srt)', upload_to='streaming/subtitles/')
    is_default = models.BooleanField('Default Subtitle', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Subtitle'
        verbose_name_plural = 'Subtitles'
        ordering = ['language']

    def __str__(self):
        target = self.movie.title if self.movie else str(self.episode)
        return f"{target} Subtitle: {self.label} ({self.language})"
