from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from groups.models import Group, GroupInvite, GroupMember, GroupRule, MemberRequest


class GroupForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Group
        fields = "__all__"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "name", "group_type", "archive_posts")
    list_filter = (
        "created_at",
        "updated_at",
        "group_type",
    )
    list_editable = (
        "group_type",
        "name",
    )
    date_hierarchy = "created_at"
    filter_horizontal = ["topics"]
    form = GroupForm
    fieldsets = (
        (
            "Group Info",
            {
                "fields": (
                    "name",
                    "description",
                ),
            },
        ),
        (
            "Group Type",
            {
                "fields": ("group_type",),
            },
        ),
        (
            "Meta",
            {
                "fields": ("topics",),
            },
        ),
        (
            "Can archive old posts?",
            {
                "fields": ("archive_posts",),
            },
        ),
    )


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "group", "member_type", "status", "user")
    list_filter = ("created_at", "updated_at", "member_type", "status")
    list_editable = ("member_type",)
    raw_id_fields = ("user",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Member Info",
            {
                "fields": (
                    "user",
                    "group",
                    "member_type",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("status",),
            },
        ),
    )


@admin.register(GroupInvite)
class GroupInviteAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "group", "user", "created_by", "invite_as")
    list_filter = (
        "created_at",
        "updated_at",
        "group",
    )
    raw_id_fields = (
        "user",
        "group",
        "created_by",
    )
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Invite Info",
            {
                "fields": (
                    "group",
                    "created_by",
                ),
            },
        ),
        (
            "Send invite to?",
            {
                "fields": ("user",),
            },
        ),
        (
            "Invite user as?",
            {
                "fields": ("invite_as",),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            # setting the user from the request object
            kwargs["initial"] = request.user.id
            # making the field readonly
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RuleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = GroupRule
        fields = "__all__"


@admin.register(GroupRule)
class GroupRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "group", "title", "rule_type")
    list_filter = ("created_at", "updated_at", "group", "rule_type")
    list_editable = ("rule_type",)
    raw_id_fields = ("group",)
    search_fields = (
        "title",
        "description",
    )
    date_hierarchy = "created_at"
    form = RuleForm
    fieldsets = (
        (
            "Rule",
            {
                "fields": (
                    "group",
                    "title",
                    "description",
                ),
            },
        ),
        (
            "Rule appplies to",
            {
                "fields": ("rule_type",),
            },
        ),
    )


@admin.register(MemberRequest)
class MemberRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "group", "user", "is_approved")
    list_filter = ("created_at", "updated_at", "group", "is_approved")
    list_editable = ("is_approved",)
    raw_id_fields = (
        "group",
        "user",
    )
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Request Info",
            {
                "fields": (
                    "group",
                    "user",
                ),
            },
        ),
        (
            "Member request approval status",
            {
                "fields": ("is_approved",),
            },
        ),
    )
