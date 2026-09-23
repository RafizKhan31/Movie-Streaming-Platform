from django.contrib import admin
from .models import VideoSource, Subtitle


@admin.register(VideoSource)
class VideoSourceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'quality', 'is_active', 'created_at')
    list_filter = ('quality', 'is_active')
    search_fields = ('movie__title', 'episode__title', 'source_url')


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'label', 'language', 'is_default', 'created_at')
    list_filter = ('language', 'is_default')
    search_fields = ('movie__title', 'episode__title', 'label')
