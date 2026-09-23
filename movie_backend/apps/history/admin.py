from django.contrib import admin
from .models import WatchHistory


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_title', 'progress_display', 'completed', 'last_watched')
    list_filter = ('completed', 'last_watched')
    search_fields = ('user__username', 'movie__title', 'episode__title')

    def item_title(self, obj):
        return obj.movie.title if obj.movie else str(obj.episode)
    item_title.short_description = 'Content'
