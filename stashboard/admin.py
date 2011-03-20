from django.contrib import admin
from stashboard.models import Service, Region, Status, Announcement, Issue, Update

class UpdateInline(admin.TabularInline):
    model = Update
    extra = 1
    readonly_fields = ["created"]


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 1
    exclude = ["closed", "resolution"]


class AnnouncementInline(admin.TabularInline):
    model = Announcement
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'region', 'status']
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['name', 'region', 'description']


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'service']
    list_filter = ['service']


class IssueAdmin(admin.ModelAdmin):
    list_filter = ['service']
    list_display = ['title', 'opened', 'is_closed', 'service']
    inlines = [UpdateInline]


admin.site.register(Service, ServiceAdmin)
admin.site.register(Region)
admin.site.register(Status)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Issue, IssueAdmin)

