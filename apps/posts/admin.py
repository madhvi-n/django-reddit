from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from posts.models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'created_at',
        'author',
        'group',
        'status',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'author',
        'status'
    )
    list_editable = ('status', 'group',)
    raw_id_fields = ('author', 'group',)
    filter_horizontal = ['tags']
    search_fields = ('title', 'content',)
    date_hierarchy = 'created_at'
    form = PostForm
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'content', 'author', 'group',),
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
