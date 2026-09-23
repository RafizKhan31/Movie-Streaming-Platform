from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField('Genre Name', max_length=100, unique=True, db_index=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, db_index=True)
    description = models.TextField('Description', blank=True)
    icon = models.CharField('Icon / FontAwesome Class', max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
