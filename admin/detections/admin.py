from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Detection
from .models import Family
from .models import Zone


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
         {'fields': ['family', 'score', 'date', 'photo_file', 'image_tag', 'verified'], 'classes': []}),
        ('Position', {'fields': ['zone', 'center_x', 'center_y', 'width', 'height'], 'classes': ['inline']}),
    ]
    list_display = ['id', 'family', 'zone', 'score', 'verified', 'date', 'image_tag']
    search_fields = ['family', 'zone', 'date']
    ordering = ['-date']
    list_filter = ['family', 'zone', 'date', 'verified']
    readonly_fields = ['image_tag']
    actions = ['mark_as_verified', 'mark_as_draft']

    @admin.action(description="Mark selected detections as verified")
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(
            request,
            ngettext(
                "%d detections was successfully marked as draft.",
                "%d detections were successfully marked as draft.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected detections as draft")
    def mark_as_draft(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(
            request,
            ngettext(
                "%d detections was successfully marked as draft.",
                "%d detections were successfully marked as draft.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Detection, DetectionAdmin)
