from comments.models import PostComment
from django.contrib import admin


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "has_children",
        "flair",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "user",
        "is_removed",
        "post",
    )
    raw_id_fields = ("mentioned_users",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Comment Info",
            {
                "fields": ("user", "_comment", "flair", "parent"),
            },
        ),
        (
            "Competition Info",
            {
                "fields": ("post",),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_removed", "is_nesting_permitted"),
            },
        ),
        ("Other", {"fields": ("mentioned_users",)}),
    )

    def has_children(self, obj):
        return PostComment.objects.filter(parent=obj).exists()

    has_children.boolean = True
