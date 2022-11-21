from django.contrib import admin
from .models import Tag, TagType


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'name',
        'tag_type'
    )
    list_filter = (
        'created_at',
        'updated_at',
        'tag_type'
    )
    search_fields = ('name',)
    raw_id_fields = ('tag_type',)
    date_hierarchy = 'created_at'


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'title',
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    search_fields = ('title',)
    date_hierarchy = 'created_at'
