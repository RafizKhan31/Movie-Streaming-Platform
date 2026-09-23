from django.db import models
from django.utils.text import slugify


class TVSeries(models.Model):
    CATEGORY_CHOICES = (
        ('tv_series', 'TV Series'),
        ('web_series', 'Web Series'),
        ('anime', 'Anime'),
        ('kids', 'Kids'),
        ('documentary', 'Documentary Series'),
    )

    title = models.CharField('Title', max_length=255, db_index=True)
    slug = models.SlugField('Slug', max_length=255, unique=True, db_index=True)
    description = models.TextField('Series Synopsis', blank=True)
    poster = models.ImageField('Poster Image', upload_to='tv/posters/', null=True, blank=True)
    poster_url = models.CharField('External Poster URL', max_length=500, blank=True)
    backdrop = models.ImageField('Backdrop Image', upload_to='tv/backdrops/', null=True, blank=True)
    backdrop_url = models.CharField('External Backdrop URL', max_length=500, blank=True)
    thumbnail = models.ImageField('Thumbnail', upload_to='tv/thumbnails/', null=True, blank=True)
    trailer_url = models.URLField('Trailer URL', blank=True, max_length=500)

    release_date = models.DateField('Release Date', null=True, blank=True)
    release_year = models.PositiveIntegerField('Release Year', null=True, blank=True, db_index=True)
    age_rating = models.CharField('Age Rating', max_length=20, default='TV-MA')

    imdb_rating = models.DecimalField('IMDb Rating', max_digits=3, decimal_places=1, default=0.0, db_index=True)
    tmdb_rating = models.DecimalField('TMDB Rating', max_digits=3, decimal_places=1, default=0.0)
    views = models.PositiveBigIntegerField('Total Views', default=0)

    featured = models.BooleanField('Featured', default=False, db_index=True)
    trending = models.BooleanField('Trending', default=False, db_index=True)
    is_active = models.BooleanField('Is Active', default=True, db_index=True)

    category = models.CharField('Category', max_length=50, choices=CATEGORY_CHOICES, default='tv_series', db_index=True)

    genres = models.ManyToManyField('genres.Genre', related_name='tv_series', blank=True)
    cast = models.ManyToManyField('movies.Person', related_name='tv_series_cast', blank=True)
    directors = models.ManyToManyField('movies.Person', related_name='tv_series_directors', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TV Series'
        verbose_name_plural = 'TV Series'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TVSeries.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if self.release_date and not self.release_year:
            self.release_year = self.release_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_poster_display(self):
        if self.poster:
            return self.poster.url
        if self.poster_url:
            return self.poster_url
        return "./Images/TheaterLogoFinal.png"

    @property
    def get_backdrop_display(self):
        if self.backdrop:
            return self.backdrop.url
        if self.backdrop_url:
            return self.backdrop_url
        return self.get_poster_display


class Season(models.Model):
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField('Season Number')
    title = models.CharField('Season Title', max_length=255, blank=True)
    description = models.TextField('Season Description', blank=True)
    poster = models.ImageField('Season Poster', upload_to='tv/seasons/', null=True, blank=True)
    release_date = models.DateField('Release Date', null=True, blank=True)

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        ordering = ['season_number']
        unique_together = ('series', 'season_number')

    def __str__(self):
        title_str = f" - {self.title}" if self.title else ""
        return f"{self.series.title} - Season {self.season_number}{title_str}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField('Episode Number')
    title = models.CharField('Episode Title', max_length=255)
    description = models.TextField('Episode Description', blank=True)
    thumbnail = models.ImageField('Thumbnail', upload_to='tv/episodes/', null=True, blank=True)
    thumbnail_url = models.CharField('External Thumbnail URL', max_length=500, blank=True)
    duration = models.CharField('Duration Label', max_length=50, blank=True, help_text="e.g. 52m")
    duration_minutes = models.PositiveIntegerField('Duration (Minutes)', default=45)
    release_date = models.DateField('Air Date', null=True, blank=True)
    video = models.FileField('Video File', upload_to='tv/videos/', null=True, blank=True)
    video_url = models.URLField('External Video Stream URL', blank=True, max_length=500)
    trailer_url = models.URLField('Episode Preview / Trailer', blank=True, max_length=500)
    views = models.PositiveBigIntegerField('Views', default=0)
    is_active = models.BooleanField('Is Active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'
        ordering = ['episode_number']
        unique_together = ('season', 'episode_number')

    def __str__(self):
        return f"S{self.season.season_number:02d}E{self.episode_number:02d} - {self.title} ({self.season.series.title})"

    @property
    def get_thumbnail_display(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.thumbnail_url:
            return self.thumbnail_url
        return self.season.series.get_poster_display
