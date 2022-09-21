from django.contrib import admin
from bookmarks.models import PostBookmark

@admin.register(PostBookmark)
class PostBookmarkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'post',
        'user',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'post',
        'user',
    )
    raw_id_fields = ('user', 'post')
    date_hierarchy = 'created_at'
