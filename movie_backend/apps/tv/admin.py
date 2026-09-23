from django.contrib import admin
from django.utils.html import format_html
from .models import TVSeries, Season, Episode


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ('episode_number', 'title', 'duration', 'release_date', 'is_active')


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    fields = ('season_number', 'title', 'release_date')


@admin.register(TVSeries)
class TVSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster_preview', 'category', 'release_year', 'imdb_rating', 'views', 'featured', 'trending', 'is_active')
    list_filter = ('category', 'is_active', 'featured', 'trending', 'genres')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres', 'cast', 'directors')
    inlines = [SeasonInline]
    ordering = ('-created_at',)

    def poster_preview(self, obj):
        url = obj.get_poster_display
        return format_html('<img src="{}" style="width: 45px; height: 60px; object-fit: cover; border-radius: 4px;" />', url)
    poster_preview.short_description = 'Poster'


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'title', 'release_date')
    list_filter = ('series',)
    search_fields = ('series__title', 'title')
    inlines = [EpisodeInline]
    ordering = ('series', 'season_number')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season_info', 'title', 'duration', 'release_date', 'views', 'is_active')
    list_filter = ('season__series', 'is_active')
    search_fields = ('title', 'season__series__title', 'description')
    ordering = ('season__series', 'season__season_number', 'episode_number')

    def season_info(self, obj):
        return f"{obj.season.series.title} S{obj.season.season_number:02d}E{obj.episode_number:02d}"
    season_info.short_description = 'Episode Info'
