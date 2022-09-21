from django.contrib import admin
from posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'author',
        'status',
        'updated_at',
        'created_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'author',
        'status'
    )
    list_editable = ('status',)
    raw_id_fields = ('author',)
    filter_horizontal = ['tags']
    search_fields = ('title', 'content',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Blog Info', {
            'fields': ('title', 'content', 'author',),
        }),
        ('Typology', {
            'fields': ('tags',),
        }),
        ('Status', {
            'fields': ('status',),
        }),
        ('Meta Info', {
            'fields': ('uuid',),
        })
    )
    readonly_fields = ('uuid',)
