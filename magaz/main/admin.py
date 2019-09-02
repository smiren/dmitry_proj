from django.contrib import admin
from .models import InfoPages, InfoPageImages

@admin.register(InfoPageImages)
class InfoPageImagesAdmin(admin.ModelAdmin):
    list_display = ['pagename', 'image', 'imagename']
    list_display_links = ['image', 'imagename']
    list_filter = ['pagename']

class InfoPageImagesInline(admin.TabularInline):
    model = InfoPageImages

@admin.register(InfoPages)
class InfoPageAdmin(admin.ModelAdmin):
    inlines = [InfoPageImagesInline]
