from django.contrib import admin

from reports.models import (
    ReportType, UserProfileReport, PostReport
)

@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('created_at','updated_at')
    date_hierarchy = 'created_at'


@admin.register(UserProfileReport)
class UserProfileReportAdmin(admin.ModelAdmin):
    list_display = (
        'reported_user',
        'report_type',
        'reporter',
        'status',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'reporter',
        'report_type',
        'reported_user',
        'status',
    )
    list_editable = ('status',)
    raw_id_fields = ('reporter', 'reported_user')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Report Info', {
            'fields': ('reporter', 'report_type', 'additional_info',),
        }),
        ('Status', {
            'fields': ('status',),
        }),
        ('Meta', {
            'fields': ('url',),
        }),
        ('Other', {
            'fields': ('reported_user',),
        })
    )


@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'report_type',
        'reporter',
        'status',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'reporter',
        'report_type',
        'post',
        'status',
    )
    list_editable = ('status',)
    raw_id_fields = ('reporter', 'post')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Report Info', {
            'fields': ('reporter', 'report_type', 'additional_info',),
        }),
        ('Status', {
            'fields': ('status',),
        }),
        ('Meta', {
            'fields': ('url',),
        }),
        ('Other', {
            'fields': ('post',),
        })
    )
