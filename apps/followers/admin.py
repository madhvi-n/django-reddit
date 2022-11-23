from django.contrib import admin
from followers.models import PostFollower, UserFollower


@admin.register(PostFollower)
class PostFollowerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'post',
        'follower',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'post',
        'follower',
    )
    raw_id_fields = ('follower', 'post')
    date_hierarchy = 'created_at'


@admin.register(UserFollower)
class UserFollowerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'followed_user',
        'follower',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'followed_user',
        'follower',
    )
    raw_id_fields = ('follower', 'followed_user')
    date_hierarchy = 'created_at'
