from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
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
    """,
)
class RoadSegmentViewSet(viewsets.ModelViewSet):
    """ViewSet for RoadSegment CRUD operations with admin/read-only permissions."""

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]

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
