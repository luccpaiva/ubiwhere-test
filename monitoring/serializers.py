from rest_framework import serializers
from .models import RoadSegment, SpeedReading
from django.utils import timezone


class RoadSegmentSerializer(serializers.ModelSerializer):
    """Serializer for RoadSegment model with validation for coordinates and length."""

    total_readings = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoadSegment
        fields = [
            "id",
            "start_longitude",
            "start_latitude",
            "end_longitude",
            "end_latitude",
            "length",
            "created_at",
            "updated_at",
            "total_readings",  # model property
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_length(self, value):
        if value <= 0:
            raise serializers.ValidationError("Length must be positive")
        return value

    def validate_start_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value

    def validate_end_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value

    def validate_start_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value

    def validate_end_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value


class SpeedReadingSerializer(serializers.ModelSerializer):
    """Serializer for SpeedReading model with traffic intensity calculation."""

    traffic_intensity = serializers.CharField(read_only=True)

    class Meta:
        model = SpeedReading
        fields = [
            "id",
            "road_segment",
            "average_speed",
            "timestamp",
            "created_at",
            "traffic_intensity",  # model property
        ]
        read_only_fields = ["id", "created_at", "traffic_intensity"]

    def validate_average_speed(self, value):
        if value <= 0:
            raise serializers.ValidationError("Average speed must be positive")
        return value

    def validate_timestamp(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Timestamp cannot be in the future")
        return value
