from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    ROLE_CHOICES = (
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('writer', 'Writer'),
        ('producer', 'Producer'),
    )
    name = models.CharField('Full Name', max_length=255, db_index=True)
    role = models.CharField('Primary Role', max_length=50, choices=ROLE_CHOICES, default='actor')
    bio = models.TextField('Biography', blank=True)
    photo = models.ImageField('Photo', upload_to='movies/people/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Person (Cast & Crew)'
        verbose_name_plural = 'People (Cast & Crew)'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.role})"


class Movie(models.Model):
    CATEGORY_CHOICES = (
        ('hollywood', 'Hollywood'),
        ('bollywood', 'Bollywood'),
        ('kids', 'Kids'),
        ('web_series', 'Web Series'),
        ('anime', 'Anime'),
        ('popular', 'Popular'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('released', 'Released'),
        ('upcoming', 'Upcoming'),
        ('in_production', 'In Production'),
    )

    title = models.CharField('Title', max_length=255, db_index=True)
    slug = models.SlugField('Slug', max_length=255, unique=True, db_index=True)
    description = models.TextField('Plot Summary', blank=True)
    poster = models.ImageField('Poster Image', upload_to='movies/posters/', null=True, blank=True)
    poster_url = models.CharField('External Poster URL', max_length=500, blank=True, help_text="Used when hosting external poster images")
    backdrop = models.ImageField('Backdrop Image', upload_to='movies/backdrops/', null=True, blank=True)
    backdrop_url = models.CharField('External Backdrop URL', max_length=500, blank=True)
    thumbnail = models.ImageField('Thumbnail', upload_to='movies/thumbnails/', null=True, blank=True)
    trailer_url = models.URLField('Trailer URL (YouTube/MP4)', blank=True, max_length=500)

    release_date = models.DateField('Release Date', null=True, blank=True)
    release_year = models.PositiveIntegerField('Release Year', null=True, blank=True, db_index=True)
    duration = models.CharField('Duration Label', max_length=50, blank=True, help_text="e.g. 2h 42m")
    duration_minutes = models.PositiveIntegerField('Duration (Minutes)', default=120)

    language = models.CharField('Audio Language', max_length=50, default='English')
    country = models.CharField('Country of Origin', max_length=100, default='USA')
    age_rating = models.CharField('Age Rating', max_length=20, default='PG-13')
    content_rating = models.CharField('Content Rating', max_length=50, blank=True)
    status = models.CharField('Status', max_length=30, choices=STATUS_CHOICES, default='released')

    imdb_rating = models.DecimalField('IMDb Rating', max_digits=3, decimal_places=1, default=0.0, db_index=True)
    tmdb_rating = models.DecimalField('TMDB Rating', max_digits=3, decimal_places=1, default=0.0)
    views = models.PositiveBigIntegerField('Total Views', default=0)

    featured = models.BooleanField('Featured on Hero Carousel', default=False, db_index=True)
    trending = models.BooleanField('Trending Now', default=False, db_index=True)
    is_active = models.BooleanField('Is Active / Published', default=True, db_index=True)

    category = models.CharField('Category', max_length=50, choices=CATEGORY_CHOICES, default='hollywood', db_index=True)

    genres = models.ManyToManyField('genres.Genre', related_name='movies', blank=True)
    cast = models.ManyToManyField(Person, through='MovieCast', related_name='acted_movies', blank=True)
    directors = models.ManyToManyField(Person, related_name='directed_movies', blank=True)
    writers = models.ManyToManyField(Person, related_name='written_movies', blank=True)

    tags = models.CharField('Tags', max_length=500, blank=True, help_text="Comma-separated keywords")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Movie.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if self.release_date and not self.release_year:
            self.release_year = self.release_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        year_str = f" ({self.release_year})" if self.release_year else ""
        return f"{self.title}{year_str}"

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


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_cast')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='cast_roles')
    character_name = models.CharField('Character / Role Name', max_length=255, blank=True)
    order = models.PositiveSmallIntegerField('Display Order', default=0)

    class Meta:
        verbose_name = 'Movie Cast Member'
        verbose_name_plural = 'Movie Cast Members'
        ordering = ['order']
        unique_together = ('movie', 'person')

    def __str__(self):
        role_info = f" as {self.character_name}" if self.character_name else ""
        return f"{self.person.name}{role_info} in {self.movie.title}"


class MovieSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    movie_name = models.CharField('Movie Name', max_length=255)
    release_year = models.PositiveIntegerField('Release Year', null=True, blank=True)
    genre = models.CharField('Genre', max_length=100, blank=True)
    description = models.TextField('Description', blank=True)
    poster = models.ImageField('Poster Upload', upload_to='submissions/posters/', null=True, blank=True)
    email = models.EmailField('Submitter Email')
    agree_terms = models.BooleanField('Agreed to Terms', default=True)
    status = models.CharField('Review Status', max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Movie Submission'
        verbose_name_plural = 'User Movie Submissions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie_name} submitted by {self.email} ({self.status})"
