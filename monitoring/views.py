from django.db.models import OuterRef, Subquery, Q
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import RoadSegment, SpeedReading
from .serializers import RoadSegmentSerializer, SpeedReadingSerializer
from .permissions import IsAdminOrReadOnly


@extend_schema(
    tags=["Road Segments"],
    description="""
    API endpoints for managing road segments.
    
    **Permissions:**
    - Anonymous users: Read-only (GET, HEAD, OPTIONS)
    - Admin users: Full access (GET, POST, PUT, PATCH, DELETE)
    
    **Filtering:**
    - Use ?traffic_intensity={elevada|média|baixa} to filter by latest reading's traffic intensity
    """,
)
class RoadSegmentViewSet(viewsets.ModelViewSet):
    """ViewSet for RoadSegment CRUD operations with admin/read-only permissions."""

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = RoadSegment.objects.all()
        traffic_intensity = self.request.query_params.get("traffic_intensity", None)

        if traffic_intensity is not None:
            # Get the latest reading's speed for each segment
            latest_reading = SpeedReading.objects.filter(
                road_segment=OuterRef("pk")
            ).order_by("-timestamp")[:1]

            queryset = queryset.annotate(
                latest_speed=Subquery(latest_reading.values("average_speed")[:1])
            )

            # Filter based on traffic intensity thresholds
            if traffic_intensity == "elevada":
                queryset = queryset.filter(
                    Q(latest_speed__isnull=False) & Q(latest_speed__lte=20)
                )
            elif traffic_intensity == "média":
                queryset = queryset.filter(
                    Q(latest_speed__isnull=False)
                    & Q(latest_speed__gt=20)
                    & Q(latest_speed__lte=50)
                )
            elif traffic_intensity == "baixa":
                queryset = queryset.filter(
                    Q(latest_speed__isnull=False) & Q(latest_speed__gt=50)
                )

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="traffic_intensity",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by traffic intensity of latest reading",
                enum=["elevada", "média", "baixa"],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    tags=["Speed Readings"],
    description="""
    API endpoints for managing speed readings.
    
    **Permissions:**
    - Anonymous users: Read-only (GET, HEAD, OPTIONS)
    - Admin users: Full access (GET, POST, PUT, PATCH, DELETE)
    
    **Filtering:**
    - Use ?road_segment={id} query parameter to filter readings by road segment
    """,
)
class SpeedReadingViewSet(viewsets.ModelViewSet):
    """ViewSet for SpeedReading CRUD operations with optional filtering by road segment."""

    queryset = SpeedReading.objects.select_related("road_segment").all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = SpeedReading.objects.select_related("road_segment").all()
        road_segment_id = self.request.query_params.get("road_segment", None)
        if road_segment_id is not None:
            queryset = queryset.filter(road_segment_id=road_segment_id)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
