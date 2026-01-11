from django.contrib import admin
from .models import RoadSegment, SpeedReading


@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "start_latitude",
        "start_longitude",
        "end_latitude",
        "end_longitude",
        "length",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["id"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("speedreadings")


@admin.register(SpeedReading)
class SpeedReadingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "road_segment",
        "average_speed",
        "traffic_intensity",
        "timestamp",
        "created_at",
    ]
    list_filter = ["timestamp", "created_at", "road_segment"]
    search_fields = ["road_segment__id", "average_speed"]
    date_hierarchy = "timestamp"
    readonly_fields = ["created_at", "traffic_intensity"]

    def traffic_intensity(self, obj):
        return obj.traffic_intensity

    traffic_intensity.short_description = "Traffic Intensity"
