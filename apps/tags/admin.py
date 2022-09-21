from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'name',
    )
    list_filter = (
        'created_at',
        'updated_at'
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
