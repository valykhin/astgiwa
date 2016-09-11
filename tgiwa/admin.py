from django.contrib import admin
from .models import Browser, Resolution, DefectType, OperatingSystem


class BrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'version', 'support_type', 'operating_system', 'creation_time')


class ResolutionAdmin(admin.ModelAdmin):
    list_display = ('width', 'height', 'aspect_ratio', 'creation_time')


class DefectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_time')


class OperatingSystemeAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'version', 'creation_time')

# Register your models here.
admin.site.register(Browser, BrowserAdmin)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(DefectType, DefectTypeAdmin)
admin.site.register(OperatingSystem, OperatingSystemeAdmin)