from django.contrib import admin

from .models import Zone
from .models import Family
from .models import Detection


class ZoneAdmin(admin.ModelAdmin):
    list_display = ['index', 'name']
    search_fields = ['index', 'name', 'date']
    ordering = ['index']


class FamilyAdmin(admin.ModelAdmin):
    list_display = ['index', 'name']
    search_fields = ['index', 'name']
    ordering = ['index']


class DetectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identification', {'fields': ['family', 'score', 'date', 'photo_file', 'image_tag'], 'classes': []}),
        ('Position', {'fields': ['zone', 'center_x', 'center_y', 'width', 'height'], 'classes': ['inline']}),
    ]
    list_display = ['id', 'family', 'zone', 'score', 'date', 'image_tag']
    search_fields = ['family', 'zone', 'date']
    ordering = ['-date']
    list_filter = ['family', 'zone', 'date']
    readonly_fields = ['image_tag']


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Detection, DetectionAdmin)