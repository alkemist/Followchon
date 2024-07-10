from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

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
        ('Identification',
         {'fields': ['family', 'score', 'verified', 'date', 'photo_file', 'image_tag'], 'classes': []}),
        ('Position', {'fields': ['zone', 'center_x', 'center_y', 'width', 'height'], 'classes': ['inline']}),
    ]
    list_display = ['id', 'family', 'zone', 'verified', 'score', 'date', 'image_tag']
    search_fields = ['family', 'zone', 'date']
    ordering = ['-date']
    list_filter = ['family', 'zone', 'date']
    readonly_fields = ['image_tag']
    actions = ["make_verified"]

    @admin.action(description="Mark selected detection as verified")
    def make_verified(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(
            request,
            ngettext(
                "%d detection was successfully marked as verified.",
                "%d detections were successfully marked as verified.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Detection, DetectionAdmin)
