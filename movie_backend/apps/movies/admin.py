from django.contrib import admin
from django.utils.html import format_html
from .models import Person, Movie, MovieCast, MovieSubmission


class MovieCastInline(admin.TabularInline):
    model = MovieCast
    extra = 1
    autocomplete_fields = ['person']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'photo_preview', 'created_at')
    list_filter = ('role',)
    search_fields = ('name', 'bio')
    ordering = ('name',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 35px; height: 35px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return format_html('<span style="color: gray;">No photo</span>')
    photo_preview.short_description = 'Photo'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'poster_preview',
        'category',
        'release_year',
        'imdb_rating',
        'views',
        'featured',
        'trending',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'is_active', 'featured', 'trending', 'release_year', 'genres')
    search_fields = ('title', 'description', 'tags', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres', 'directors', 'writers')
    inlines = [MovieCastInline]
    actions = ['mark_featured', 'mark_trending', 'mark_active', 'mark_inactive']
    ordering = ('-created_at',)

    def poster_preview(self, obj):
        url = obj.get_poster_display
        return format_html('<img src="{}" style="width: 45px; height: 60px; object-fit: cover; border-radius: 4px;" />', url)
    poster_preview.short_description = 'Poster'

    @admin.action(description="Mark selected movies as Featured")
    def mark_featured(self, request, queryset):
        queryset.update(featured=True)

    @admin.action(description="Mark selected movies as Trending")
    def mark_trending(self, request, queryset):
        queryset.update(trending=True)

    @admin.action(description="Mark selected movies as Active")
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected movies as Inactive")
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(MovieSubmission)
class MovieSubmissionAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'release_year', 'genre', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('movie_name', 'email', 'description')
    actions = ['approve_submissions', 'reject_submissions']

    @admin.action(description="Approve selected submissions")
    def approve_submissions(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Reject selected submissions")
    def reject_submissions(self, request, queryset):
        queryset.update(status='rejected')
