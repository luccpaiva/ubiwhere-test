from django.db import models


class RoadSegment(models.Model):
    start_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    start_latitude = models.DecimalField(max_digits=10, decimal_places=7)

    end_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=7)

    # Length in meters
    length = models.DecimalField(max_digits=10, decimal_places=2)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Segment {self.id}: ({self.start_latitude}, {self.start_longitude}) to ({self.end_latitude}, {self.end_longitude})"

    @property
    def total_readings(self):
        return self.speedreadings.count()


class SpeedReading(models.Model):
    # Link to road segment
    road_segment = models.ForeignKey(
        RoadSegment, on_delete=models.CASCADE, related_name="speedreadings"
    )

    average_speed = models.DecimalField(max_digits=5, decimal_places=2)

    timestamp = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reading {self.id}: {self.average_speed} km/h at {self.timestamp}"

    @property
    def traffic_intensity(self):
        # Consider a better design for this, to allow for easy setting of thresholds
        speed = float(self.average_speed)
        if speed <= 20:
            return "elevada"
        elif speed <= 50:
            return "média"
        else:
            return "baixa"
