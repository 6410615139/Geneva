from django.contrib import admin
from .models import Sector, Result, Member, Announcement

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'month', 'image_preview')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 100px;"/>'
        return "No Image"
    image_preview.allow_tags = True  # Allow HTML in Django Admin
    image_preview.short_description = "Image Preview"

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'sector', 'month', 'status', 'rain_image_preview', 'suggestion_image_preview')
    search_fields = ('sector__name', 'month')
    list_filter = ('status',)
    readonly_fields = ('rain_image_preview', 'suggestion_image_preview')

    def rain_image_preview(self, obj):
        if obj.rain_image:
            return f'<img src="{obj.rain_image.url}" style="max-width: 100px;"/>'
        return "No Image"
    rain_image_preview.allow_tags = True
    rain_image_preview.short_description = "Rain Image Preview"

    def suggestion_image_preview(self, obj):
        if obj.suggestion_image:
            return f'<img src="{obj.suggestion_image.url}" style="max-width: 100px;"/>'
        return "No Image"
    suggestion_image_preview.allow_tags = True
    suggestion_image_preview.short_description = "Suggestion Image Preview"

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ('phone',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('message',) 

